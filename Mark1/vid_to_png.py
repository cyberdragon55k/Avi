import subprocess
import os
from datetime import timedelta

# Configuration
input_video = "output.mp4"  # Double-check this path!
output_dir = "screenshots"
interval_seconds = 300  # 5 minutes

os.makedirs(output_dir, exist_ok=True)

def get_duration(filename):
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        filename
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Error getting duration: {e}")
        print(f"FFprobe stderr: {result.stderr}")  # Debugging line
        return None

duration = get_duration(input_video)

# Check if video exists and has valid duration
if not os.path.exists(input_video):
    print(f"Error: Input video '{input_video}' not found.")
elif duration is None:
    print("Failed to read video duration.")
elif duration < interval_seconds:
    print(f"Video is too short ({duration}s < {interval_seconds}s).")
else:
    # Fixed escape sequence (use raw string)
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", input_video,
        "-vf", rf"select='not(mod(t\,{interval_seconds}))',setpts=N/TB",
        "-vsync", "vfr",
        "-q:v", "2",
        os.path.join(output_dir, "screenshot_%03d.png")
    ]

    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"Screenshots saved to {output_dir}/")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg failed: {e}")
    except FileNotFoundError:
        print("FFmpeg not installed. Download it from https://ffmpeg.org/")