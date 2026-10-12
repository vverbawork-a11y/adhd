"""Exercise the cloud video tools; this is not a hardware performance test."""

import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    for executable in ("ffmpeg", "ffprobe"):
        if shutil.which(executable) is None:
            raise SystemExit(f"Missing prerequisite: {executable}")

    with tempfile.TemporaryDirectory(prefix="adhd-video-check-") as directory:
        output = Path(directory) / "overlay.mp4"
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-n",
            "-f", "lavfi", "-i", "testsrc2=size=320x240:rate=60",
            "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000",
            "-filter_complex",
            "[1:a]showwaves=s=320x80:mode=line:rate=60:colors=0x62ffad,"
            "format=rgba[w];[0:v][w]overlay=0:160[v]",
            "-map", "[v]", "-t", "2", "-an", "-c:v", "libx264",
            "-pix_fmt", "yuv420p", str(output),
        ], check=True)
        probe = subprocess.run([
            "ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
            "-show_entries", "stream=codec_name,width,height,r_frame_rate,nb_read_frames",
            "-of", "json", str(output),
        ], check=True, capture_output=True, text=True)
        stream = json.loads(probe.stdout)["streams"][0]
        expected = {
            "codec_name": "h264", "width": 320, "height": 240,
            "r_frame_rate": "60/1", "nb_read_frames": "120",
        }
        if any(stream.get(key) != value for key, value in expected.items()):
            raise SystemExit(f"Unexpected video properties: {stream}")
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-xerror",
            "-i", str(output), "-f", "null", "-",
        ], check=True)
        hashes = subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(output),
            "-map", "0:v:0", "-f", "framemd5", "-",
        ], check=True, capture_output=True, text=True)
        frames = [line.rsplit(",", 1)[-1].strip() for line in hashes.stdout.splitlines()
                  if line and not line.startswith("#")]
        if len(frames) != 120 or len(set(frames)) != 120:
            raise SystemExit("Expected 120 distinct decoded test frames.")
        print("PASS: synthetic waveform composited over video; H.264, 320x240, 60 fps, 120 distinct frames; decode succeeded.")
        print("This validates the cloud tools, not live audio, CV timing, or Raspberry Pi performance.")


if __name__ == "__main__":
    main()
