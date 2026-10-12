#!/usr/bin/env python3
"""Offline media preparation for a future automatic SD-card importer.

This does not implement playback or promise hardware decoding. Sources are read
only; manifests and converted videos belong in a separate writable cache.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import statistics
import subprocess
import tempfile
from dataclasses import dataclass
from fractions import Fraction
from typing import Any


SETTINGS = {
    "version": 2,
    "codec": "libx264",
    "pixel_format": "yuv420p",
    "max_width": 1920,
    "max_height": 1080,
    "max_fps": 60,
    "crf": 20,
    "preset": "veryfast",
    "threads": 2,
    "timestamps": "preserve; cap rates above 60; never interpolate",
}
VIDEO_EXTENSIONS = {
    ".mp4", ".m4v", ".mov", ".mkv", ".webm", ".avi", ".mpg", ".mpeg",
    ".ts", ".mts", ".m2ts", ".ogv",
}
FORMAT_WHITELIST = "mov,matroska,webm,avi,mpeg,mpegts,ogg"


class MediaError(Exception):
    """A single file cannot be imported; other files can still be processed."""


def parse_rate(value: Any) -> Fraction | None:
    """Keep rational rates such as 60000/1001 exact, ignoring unavailable rates."""
    try:
        rate = Fraction(str(value))
    except (ValueError, ZeroDivisionError, TypeError):
        return None
    return rate if 0 < rate <= 1000 else None


def finite_number(value: Any) -> float | None:
    try:
        number = float(value)
    except (ValueError, TypeError):
        return None
    return number if number == number and abs(number) != float("inf") else None


@dataclass(frozen=True)
class Probe:
    codec: str
    pixel_format: str
    width: int
    height: int
    fps: Fraction
    declared_fps: Fraction | None
    time_base: str | None
    start_time: float | None
    duration: float | None
    timestamp_sample: tuple[float, ...]
    sample_aspect_ratio: str | None = None
    rotation_degrees: float | None = None
    color_transfer: str | None = None
    color_primaries: str | None = None
    color_space: str | None = None
    hdr_metadata_detected: bool = False

    @property
    def sampled_fps(self) -> float | None:
        deltas = [b - a for a, b in zip(self.timestamp_sample, self.timestamp_sample[1:])
                  if b > a]
        return 1 / statistics.median(deltas) if deltas else None

    def as_dict(self) -> dict[str, Any]:
        return {
            "codec": self.codec,
            "pixel_format": self.pixel_format,
            "width": self.width,
            "height": self.height,
            "fps": str(self.fps),
            "fps_decimal": float(self.fps),
            "declared_fps": str(self.declared_fps) if self.declared_fps else None,
            "time_base": self.time_base,
            "start_time_seconds": self.start_time,
            "duration_seconds": self.duration,
            "timestamp_sample_seconds": list(self.timestamp_sample),
            "sampled_fps": self.sampled_fps,
            "sample_aspect_ratio": self.sample_aspect_ratio,
            "rotation_degrees": self.rotation_degrees,
            "color_transfer": self.color_transfer,
            "color_primaries": self.color_primaries,
            "color_space": self.color_space,
            "hdr_metadata_detected": self.hdr_metadata_detected,
            "timing_scope": "stream metadata and first two seconds; full-file cadence is not verified",
        }


def parse_probe(document: Any) -> Probe:
    if not isinstance(document, dict):
        raise MediaError("FFprobe returned an invalid document.")
    streams = document.get("streams")
    if not isinstance(streams, list) or not streams or not isinstance(streams[0], dict):
        raise MediaError("No readable video stream found.")
    stream = streams[0]
    try:
        width, height = int(stream["width"]), int(stream["height"])
    except (KeyError, ValueError, TypeError):
        raise MediaError("Video dimensions are missing or invalid.") from None
    if width <= 0 or height <= 0 or width * height > 100_000_000:
        raise MediaError("Video dimensions are unsupported.")
    codec, pixel_format = stream.get("codec_name"), stream.get("pix_fmt")
    if not isinstance(codec, str) or not codec or not isinstance(pixel_format, str):
        raise MediaError("Video codec or pixel format is unavailable.")
    fps = parse_rate(stream.get("avg_frame_rate")) or parse_rate(stream.get("r_frame_rate"))
    if fps is None:
        raise MediaError("A valid presentation frame rate is unavailable.")
    frames = document.get("frames", [])
    if not isinstance(frames, list):
        frames = []
    timestamps = tuple(t for frame in frames[:180] if isinstance(frame, dict)
                       if (t := finite_number(frame.get("best_effort_timestamp_time"))) is not None)
    format_info = document.get("format", {})
    if not isinstance(format_info, dict):
        format_info = {}
    side_data = stream.get("side_data_list", [])
    if not isinstance(side_data, list):
        side_data = []
    tags = stream.get("tags", {})
    if not isinstance(tags, dict):
        tags = {}
    rotation = finite_number(tags.get("rotate"))
    hdr = stream.get("color_transfer") in {"smpte2084", "arib-std-b67"}
    for item in side_data:
        if not isinstance(item, dict):
            continue
        angle = finite_number(item.get("rotation"))
        if angle is not None:
            rotation = angle
        side_type = str(item.get("side_data_type", "")).lower()
        hdr = hdr or any(marker in side_type for marker in
                         ("dovi", "dolby", "hdr", "mastering display", "content light level"))
    return Probe(
        codec, pixel_format, width, height, fps,
        parse_rate(stream.get("r_frame_rate")), stream.get("time_base"),
        finite_number(stream.get("start_time", format_info.get("start_time"))),
        finite_number(stream.get("duration", format_info.get("duration"))), timestamps,
        stream.get("sample_aspect_ratio"), rotation, stream.get("color_transfer"),
        stream.get("color_primaries"), stream.get("color_space"), hdr,
    )


def run_process(command: list[str], timeout: float, operation: str) -> subprocess.CompletedProcess[str]:
    if not 0 < timeout <= 3600:
        raise MediaError("Process timeout must be between 0 and 3600 seconds.")
    try:
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace",
                                timeout=timeout, check=False, shell=False)
    except subprocess.TimeoutExpired:
        raise MediaError(f"{operation} exceeded its {timeout:g}-second time limit.") from None
    except OSError:
        raise MediaError(f"{operation} could not start; install FFmpeg and FFprobe.") from None
    if result.returncode:
        # Tool output can contain arbitrary media metadata. Do not copy it into
        # a persisted manifest or expose it as a diagnostic.
        raise MediaError(f"{operation} failed (exit {result.returncode}); file may be corrupt or unsupported.")
    return result


def probe_media(source: Path, timeout: float = 300) -> Probe:
    command = [
        "ffprobe", "-v", "error", "-threads", "2",
        "-protocol_whitelist", "file,pipe", "-format_whitelist", FORMAT_WHITELIST,
        "-select_streams", "v:0", "-read_intervals", "%+2", "-show_frames",
        "-show_entries",
        "stream=codec_name,pix_fmt,width,height,avg_frame_rate,r_frame_rate,time_base,start_time,duration,"
        "sample_aspect_ratio,color_transfer,color_primaries,color_space:"
        "stream_side_data=side_data_type,rotation:stream_tags=rotate:"
        "format=start_time,duration:frame=best_effort_timestamp_time",
        "-of", "json", str(source.resolve()),
    ]
    result = run_process(command, timeout, "FFprobe")
    try:
        document = json.loads(result.stdout)
    except (ValueError, TypeError):
        raise MediaError("FFprobe returned invalid JSON.") from None
    return parse_probe(document)


def direct_candidate(probe: Probe) -> bool:
    """A conservative file-format candidate, not a playback/acceleration test."""
    return (
        probe.codec == "h264"
        and not probe.hdr_metadata_detected
        and probe.pixel_format in {"yuv420p", "yuvj420p", "nv12"}
        and probe.width <= SETTINGS["max_width"]
        and probe.height <= SETTINGS["max_height"]
        and probe.fps <= SETTINGS["max_fps"]
    )


def motion_flags(probe: Probe) -> dict[str, Any]:
    below_60 = probe.fps < 60
    note = ("Source presentation rate is below 60 fps. Conversion preserves it; "
            "repeating frames at 60 Hz would not create true 60 fps motion.") if below_60 else (
        "Source timing reports at least 60 fps. Unique captured motion is not verified; "
        "the importer does not generate interpolated frames."
    )
    sampled = probe.sampled_fps
    timing_mismatch = sampled is not None and abs(sampled - float(probe.fps)) > float(probe.fps) * 0.05
    return {
        "source_below_60_fps": below_60,
        "source_60_class": Fraction(599, 10) <= probe.fps <= 60,
        "source_rate_above_60_fps": probe.fps > 60,
        "motion_verified": False,
        "timing_sample_differs_from_average": timing_mismatch,
        "peak_frame_rate_verified": False,
        "note": note,
    }


def source_digest(source: Path) -> str:
    digest = hashlib.sha256()
    with source.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def cache_key(digest: str) -> str:
    settings = json.dumps(SETTINGS, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256((digest + "\0" + settings).encode("utf-8")).hexdigest()


def conversion_command(source: Path, destination: Path, probe: Probe) -> list[str]:
    filters = (
        "scale=w='min(1920,iw)':h='min(1080,ih)':"
        "force_original_aspect_ratio=decrease:force_divisible_by=2:out_range=tv"
    )
    if probe.fps > SETTINGS["max_fps"]:
        filters += ",fps=60"
    return [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
        "-threads", "2", "-filter_threads", "2",
        "-protocol_whitelist", "file,pipe", "-format_whitelist", FORMAT_WHITELIST,
        "-i", str(source.resolve()), "-map", "0:v:0", "-an", "-sn", "-dn",
        "-map_metadata", "-1", "-vf", filters, "-fps_mode", "passthrough",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-color_range", "tv", "-preset", "veryfast",
        "-crf", "20", "-threads", "2", "-movflags", "+faststart", str(destination),
    ]


def separate_cache(source_folder: Path, cache_folder: Path) -> tuple[Path, Path]:
    source_folder, cache_folder = source_folder.resolve(), cache_folder.resolve()
    if not source_folder.is_dir():
        raise ValueError("The source must be an existing media folder.")
    if cache_folder == source_folder or source_folder in cache_folder.parents:
        raise ValueError("The cache must be outside the source folder; the source is read only.")
    return source_folder, cache_folder


def import_file(source: Path, cache_folder: Path, timeout: float = 300) -> dict[str, Any]:
    source = source.resolve()
    _, cache_folder = separate_cache(source.parent, cache_folder)
    digest = source_digest(source)
    probe = probe_media(source, timeout)
    result: dict[str, Any] = {
        "source": str(source), "source_sha256": digest,
        "source_probe": probe.as_dict(), "motion": motion_flags(probe),
        "hardware_acceleration_verified": False,
    }
    if probe.hdr_metadata_detected:
        result.update(status="unsupported", error="HDR/Dolby Vision media is unsupported; SDR tone mapping is not implemented.")
        return result
    if direct_candidate(probe):
        verify_source_unchanged(source, digest)
        result.update(status="direct_candidate", playback_path=str(source),
                      output_probe=probe.as_dict())
        return result

    cache_folder.mkdir(parents=True, exist_ok=True)
    destination = cache_folder / (cache_key(digest) + ".mp4")
    if destination.exists():
        try:
            cached_probe = probe_media(destination, timeout)
            if direct_candidate(cached_probe):
                verify_source_unchanged(source, digest)
                result.update(status="cached", playback_path=str(destination),
                              output_probe=cached_probe.as_dict())
                return result
        except MediaError:
            pass  # A corrupt cache is replaced atomically; source stays untouched.

    descriptor, temporary_name = tempfile.mkstemp(prefix=".import-", suffix=".mp4", dir=cache_folder)
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        run_process(conversion_command(source, temporary, probe), timeout, "FFmpeg conversion")
        output_probe = probe_media(temporary, timeout)
        if not direct_candidate(output_probe):
            raise MediaError("Converted output does not meet the cache format requirements.")
        verify_source_unchanged(source, digest)
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)
    result.update(status="converted", playback_path=str(destination),
                  output_probe=output_probe.as_dict())
    return result


def verify_source_unchanged(source: Path, digest: str) -> None:
    if source_digest(source) != digest:
        raise MediaError("Source changed during import; retry after the copy has finished.")


def atomic_manifest(path: Path, document: dict[str, Any]) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=".manifest-", suffix=".json", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(document, stream, ensure_ascii=True, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def import_folder(source_folder: Path, cache_folder: Path, *, timeout: float = 300,
                  recursive: bool = False) -> dict[str, Any]:
    source_folder, cache_folder = separate_cache(source_folder, cache_folder)
    if not 0 < timeout <= 3600:
        raise ValueError("Process timeout must be between 0 and 3600 seconds.")
    cache_folder.mkdir(parents=True, exist_ok=True)
    candidates = source_folder.rglob("*") if recursive else source_folder.iterdir()
    sources = sorted((p for p in candidates if p.is_file() and p.suffix.lower() in VIDEO_EXTENSIONS),
                     key=lambda p: str(p))
    entries = []
    for source in sources:
        # Do not follow an SD-card symlink into another folder or the writable cache.
        if not source.resolve().is_relative_to(source_folder):
            entries.append({"source": str(source), "status": "error", "error": "External symlink skipped."})
            continue
        try:
            entries.append(import_file(source, cache_folder, timeout))
        except (MediaError, OSError, ValueError) as error:
            message = str(error) if isinstance(error, MediaError) else "File could not be read or imported."
            entries.append({"source": str(source), "status": "error", "error": message})
    manifest = {
        "manifest_version": 1, "settings": SETTINGS, "source_folder": str(source_folder),
        "cache_folder": str(cache_folder), "playback_engine_implemented": False,
        "entries": entries,
    }
    atomic_manifest(cache_folder / "manifest.json", manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_folder", type=Path)
    parser.add_argument("--cache", type=Path, required=True, help="Writable cache outside the source/SD folder")
    parser.add_argument("--timeout", type=float, default=300, help="Time limit per FFmpeg/FFprobe process")
    parser.add_argument("--recursive", action="store_true")
    args = parser.parse_args()
    try:
        manifest = import_folder(args.source_folder, args.cache, timeout=args.timeout, recursive=args.recursive)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(manifest, ensure_ascii=True, indent=2))
    return 1 if any(entry["status"] in {"error", "unsupported"} for entry in manifest["entries"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
