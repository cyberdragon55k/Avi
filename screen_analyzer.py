import os
import subprocess
import base64
import requests
import json
from datetime import datetime

# === CONFIG ===
API_KEY = "AIzaSyCNC7o8jOGZzBdb7KHKHBQOj29qwpJg7OI"  # Replace with your Gemini API key
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key={API_KEY}"
HEADERS = {"Content-Type": "application/json"}

RECORD_DURATION = 60  # Seconds to record
FRAME_INTERVAL = 10   # Seconds between screenshots
OUTPUT_DIR = "screenshots"
ANALYSIS_FILE = "frame_analysis.json"

def record_screen():
    print("🟢 Starting screen recording...")
    cmd = [
        "ffmpeg", "-y", "-f", "gdigrab",
        "-framerate", "30", "-i", "desktop",
        "-t", str(RECORD_DURATION), "output.mp4"
    ]
    subprocess.run(cmd, check=True)
    print("✅ Recording saved as output.mp4")

def extract_frames():
    print("\n🟡 Extracting frames...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    cmd = [
        "ffmpeg", "-i", "output.mp4",
        "-vf", f"fps=1/{FRAME_INTERVAL}",
        "-vsync", "vfr",
        f"{OUTPUT_DIR}/frame_%03d.png"
    ]
    subprocess.run(cmd, check=True)
    extracted = len([f for f in os.listdir(OUTPUT_DIR) if f.endswith('.png')])
    print(f"✅ {extracted} frames extracted")

def classify_image(image_path):
    with open(image_path, "rb") as img_file:
        base64_img = base64.b64encode(img_file.read()).decode("utf-8")

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": "image/png",
                            "data": base64_img
                        }
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()
        if "candidates" in data:
            return data['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"⚠️ Unexpected response: {json.dumps(data)}"
    except Exception as e:
        return f"❌ Error: {e}"

def analyze_frames():
    print("\n🔵 Analyzing frames...")
    results = []

    for frame in sorted(os.listdir(OUTPUT_DIR)):
        if frame.lower().endswith(".png"):
            path = os.path.join(OUTPUT_DIR, frame)
            result = classify_image(path)
            print(f"\n📸 {frame}:")
            print(f"📝 {result}")
            results.append({
                "frame": frame,
                "timestamp": datetime.now().isoformat(),
                "description": result
            })

    with open(ANALYSIS_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n🗂️ Analysis saved to {ANALYSIS_FILE}")

def main():
    record_screen()
    extract_frames()
    analyze_frames()
    print("\n🎉 Analysis complete!")

if __name__ == "__main__":
    main()
