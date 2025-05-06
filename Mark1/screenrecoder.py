import subprocess
import time

# Start recording
command = [
    "ffmpeg",
    "-f", "gdigrab",
    "-framerate", "30",
    "-i", "desktop",
    "output.mp4"
]
process = subprocess.Popen(command)

# Let it record for 60 seconds
time.sleep(60)

# Stop recording
process.terminate()