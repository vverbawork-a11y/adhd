"""Importer checks, including actual tiny video fixtures when FFmpeg is available."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from fractions import Fraction
from unittest import mock

from tools import import_media as media


def probe_document(*, codec="h264", pixel_format="yuv420p", fps="60/1", declared="60/1"):
    return {
        "streams": [{"codec_name": codec, "pix_fmt": pixel_format, "width": 320,
                     "height": 240, "avg_frame_rate": fps, "r_frame_rate": declared,
                     "time_base": "1/60000", "start_time": "0", "duration": "2"}],
        "frames": [{"best_effort_timestamp_time": "0"},
                   {"best_effort_timestamp_time": "0.016667"}],
    }


class ProbeTests(unittest.TestCase):
    def test_invalid_probe_and_rates(self):
        for document in [None, [], {}, {"streams": []}, {"streams": [{"width": 0}]}]:
            with self.subTest(document=document), self.assertRaises(media.MediaError):
                media.parse_probe(document)
        for value in [None, "0/0", "1/0", "N/A", "-30/1", "NaN", "1001/1"]:
            self.assertIsNone(media.parse_rate(value))

    def test_fractional_frame_rate_and_timestamps(self):
        probe = media.parse_probe(probe_document(fps="60000/1001", declared="60000/1001"))
        self.assertEqual(probe.fps, Fraction(60000, 1001))
        self.assertEqual(probe.as_dict()["fps"], "60000/1001")
        self.assertEqual(probe.time_base, "1/60000")
        self.assertEqual(probe.timestamp_sample, (0.0, 0.016667))
        self.assertTrue(media.motion_flags(probe)["source_below_60_fps"])
        self.assertTrue(media.motion_flags(probe)["source_60_class"])

    def test_slow_motion_uses_presentation_rate(self):
        document = probe_document(fps="30/1", declared="120/1")
        document["frames"][1]["best_effort_timestamp_time"] = "0.033333"
        probe = media.parse_probe(document)
        self.assertEqual(probe.fps, 30)
        self.assertEqual(probe.declared_fps, 120)
        self.assertTrue(media.motion_flags(probe)["source_below_60_fps"])
        command = media.conversion_command(Path("odd name; $(touch NEVER).avi"), Path("cache.mp4"), probe)
        self.assertNotIn("-r", command)
        self.assertNotIn("fps=60", command[command.index("-vf") + 1])
        self.assertNotIn("minterpolate", " ".join(command))

    def test_direct_candidate_is_conservative(self):
        self.assertTrue(media.direct_candidate(media.parse_probe(probe_document())))
        self.assertFalse(media.direct_candidate(media.parse_probe(probe_document(codec="av1"))))
        self.assertFalse(media.direct_candidate(media.parse_probe(probe_document(pixel_format="yuv420p10le"))))
        self.assertFalse(media.direct_candidate(media.parse_probe(probe_document(fps="120/1"))))
        document = probe_document()
        document["streams"][0]["width"] = 3840
        self.assertFalse(media.direct_candidate(media.parse_probe(document)))

    def test_rotation_and_anamorphic_aspect_are_preserved(self):
        document = probe_document(codec="mjpeg")
        document["streams"][0].update(sample_aspect_ratio="16:15", side_data_list=[
            {"side_data_type": "Display Matrix", "rotation": -90}
        ])
        probe = media.parse_probe(document)
        self.assertEqual(probe.as_dict()["rotation_degrees"], -90)
        self.assertEqual(probe.as_dict()["sample_aspect_ratio"], "16:15")
        self.assertNotIn("setsar=1", " ".join(media.conversion_command(Path("in.avi"), Path("out.mp4"), probe)))

    def test_hdr_and_dolby_vision_are_not_sdr_candidates(self):
        for metadata in [{"color_transfer": "smpte2084"}, {"color_transfer": "arib-std-b67"},
                         {"side_data_list": [{"side_data_type": "DOVI configuration record"}]}]:
            document = probe_document()
            document["streams"][0].update(metadata)
            probe = media.parse_probe(document)
            self.assertTrue(probe.hdr_metadata_detected)
            self.assertFalse(media.direct_candidate(probe))

    def test_cache_key_tracks_content_and_settings_version(self):
        first = media.cache_key("a" * 64)
        self.assertNotEqual(first, media.cache_key("b" * 64))
        with mock.patch.dict(media.SETTINGS, {"version": 99}):
            self.assertNotEqual(first, media.cache_key("a" * 64))

    def test_process_timeout_and_failure_do_not_dump_metadata(self):
        with mock.patch.object(media.subprocess, "run", side_effect=subprocess.TimeoutExpired("ffprobe", 1)):
            with self.assertRaisesRegex(media.MediaError, "time limit"):
                media.run_process(["ffprobe"], 1, "FFprobe")
        failed = subprocess.CompletedProcess(["ffprobe"], 1, "", "arbitrary secret-bearing metadata")
        with mock.patch.object(media.subprocess, "run", return_value=failed):
            with self.assertRaises(media.MediaError) as caught:
                media.run_process(["ffprobe"], 1, "FFprobe")
            self.assertNotIn("metadata", str(caught.exception))


class FolderTests(unittest.TestCase):
    def test_source_cache_overlap_is_rejected_before_writes(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "sd"
            source.mkdir()
            with self.assertRaises(ValueError):
                media.import_folder(source, source / "cache")
            self.assertEqual(list(source.iterdir()), [])

    def test_invalid_file_does_not_abort_batch_or_change_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            source, cache = Path(temporary) / "sd", Path(temporary) / "cache"
            source.mkdir()
            bad, good = source / "bad.mp4", source / "good.mp4"
            bad.write_bytes(b"bad input")
            good.write_bytes(b"source content")
            before = {p.name: p.read_bytes() for p in source.iterdir()}
            with mock.patch.object(media, "probe_media", side_effect=[
                media.MediaError("Unreadable file."), media.parse_probe(probe_document())
            ]):
                manifest = media.import_folder(source, cache)
            self.assertEqual([e["status"] for e in manifest["entries"]], ["error", "direct_candidate"])
            self.assertEqual({p.name: p.read_bytes() for p in source.iterdir()}, before)
            self.assertTrue((cache / "manifest.json").is_file())
            self.assertFalse((source / "manifest.json").exists())

    def test_failed_conversion_removes_temporary_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            source, cache = Path(temporary) / "sd", Path(temporary) / "cache"
            source.mkdir()
            clip = source / "clip.avi"
            clip.write_bytes(b"unchanged")
            with mock.patch.object(media, "probe_media", return_value=media.parse_probe(probe_document(codec="mjpeg"))), \
                 mock.patch.object(media, "run_process", side_effect=media.MediaError("Conversion failed.")):
                manifest = media.import_folder(source, cache)
            self.assertEqual(manifest["entries"][0]["status"], "error")
            self.assertEqual(list(cache.glob("*.mp4")), [])
            self.assertEqual(list(cache.glob(".import-*")), [])
            self.assertEqual(clip.read_bytes(), b"unchanged")

    def test_hdr_is_reported_unsupported_without_conversion(self):
        with tempfile.TemporaryDirectory() as temporary:
            source, cache = Path(temporary) / "sd", Path(temporary) / "cache"
            source.mkdir()
            clip = source / "hdr.mp4"
            clip.write_bytes(b"source")
            document = probe_document()
            document["streams"][0]["color_transfer"] = "smpte2084"
            with mock.patch.object(media, "probe_media", return_value=media.parse_probe(document)), \
                 mock.patch.object(media, "run_process") as process:
                result = media.import_folder(source, cache)["entries"][0]
            self.assertEqual(result["status"], "unsupported")
            process.assert_not_called()
            self.assertEqual(clip.read_bytes(), b"source")

    def test_source_mutation_is_rejected_before_accepting_direct_path(self):
        with tempfile.TemporaryDirectory() as temporary:
            source, cache = Path(temporary) / "sd", Path(temporary) / "cache"
            source.mkdir()
            clip = source / "clip.mp4"
            clip.write_bytes(b"original")
            def mutate_during_probe(*args):
                clip.write_bytes(b"changed while importing")
                return media.parse_probe(probe_document())
            with mock.patch.object(media, "probe_media", side_effect=mutate_during_probe):
                result = media.import_folder(source, cache)["entries"][0]
            self.assertEqual(result["status"], "error")
            self.assertIn("Source changed", result["error"])
            self.assertEqual(list(cache.glob("*.mp4")), [])


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg/FFprobe required")
class FFmpegIntegrationTests(unittest.TestCase):
    def create_clip(self, path, *, rate, encoder):
        command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
                   "-f", "lavfi", "-i", f"testsrc2=size=64x48:rate={rate}",
                   "-t", "0.25", "-an", "-c:v", encoder, "-threads", "2", str(path)]
        subprocess.run(command, capture_output=True, check=True, timeout=30)

    def test_native_60_and_mjpeg_conversion_with_awkward_filename(self):
        with tempfile.TemporaryDirectory() as temporary:
            source, cache = Path(temporary) / "sd", Path(temporary) / "cache"
            source.mkdir()
            native = source / "native60.mp4"
            conversion = source / "convert 'кадр'; $(touch SHOULD_NOT_EXIST).avi"
            broken = source / "broken.mp4"
            self.create_clip(native, rate="60", encoder="libx264")
            self.create_clip(conversion, rate="30000/1001", encoder="mjpeg")
            broken.write_bytes(b"not a video")
            before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in source.iterdir()}
            manifest = media.import_folder(source, cache, timeout=30)
            entries = {Path(e["source"]).name: e for e in manifest["entries"]}
            self.assertEqual(entries[native.name]["status"], "direct_candidate")
            self.assertEqual(entries[native.name]["source_probe"]["fps"], "60")
            self.assertFalse(entries[native.name]["motion"]["source_below_60_fps"])
            converted = entries[conversion.name]
            self.assertEqual(converted["status"], "converted", converted)
            self.assertEqual(converted["output_probe"]["codec"], "h264")
            self.assertEqual(converted["output_probe"]["pixel_format"], "yuv420p")
            self.assertEqual(converted["output_probe"]["fps"], "30000/1001")
            self.assertTrue(converted["motion"]["source_below_60_fps"])
            self.assertEqual(entries[broken.name]["status"], "error")
            self.assertEqual({p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in source.iterdir()}, before)
            self.assertEqual(len(list(cache.glob("*.mp4"))), 1)
            self.assertEqual(list(source.glob("SHOULD_NOT_EXIST")), [])
            self.assertEqual(json.loads((cache / "manifest.json").read_text())["entries"], manifest["entries"])
            second = media.import_folder(source, cache, timeout=30)
            reused = next(e for e in second["entries"] if e["source"] == str(conversion))
            self.assertEqual(reused["status"], "cached")
            self.assertEqual(len(list(cache.glob("*.mp4"))), 1)

    def test_av1_conversion_preserves_5994_rate(self):
        with tempfile.TemporaryDirectory() as temporary:
            source, cache = Path(temporary) / "sd", Path(temporary) / "cache"
            source.mkdir()
            clip = source / "native5994-av1.mp4"
            self.create_clip(clip, rate="60000/1001", encoder="libaom-av1")
            before = hashlib.sha256(clip.read_bytes()).hexdigest()
            result = media.import_folder(source, cache, timeout=30)["entries"][0]
            self.assertEqual(result["status"], "converted", result)
            self.assertEqual(result["source_probe"]["codec"], "av1")
            self.assertEqual(result["source_probe"]["fps"], "60000/1001")
            self.assertEqual(result["output_probe"]["fps"], "60000/1001")
            self.assertEqual(result["output_probe"]["codec"], "h264")
            self.assertTrue(result["motion"]["source_below_60_fps"])
            self.assertEqual(hashlib.sha256(clip.read_bytes()).hexdigest(), before)


if __name__ == "__main__":
    unittest.main()
