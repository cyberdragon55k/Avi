import os
import time
from datetime import datetime
import mss
import csv
from PIL import Image
import ollama

CAPTURE_INTERVAL = 10
MODEL_NAME = "moondream"
CSV_FILE = "productivity_log.csv"

SCREENSHOT_DIR = "screenshots"
TEMP_IMAGE_PATH = os.path.join(SCREENSHOT_DIR, "current_screen.png")

if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)
    print(f"📁 Created missing directory: {SCREENSHOT_DIR}")

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Activity_Summary"])
    print(f"📄 Created spreadsheet log: {CSV_FILE}")


def capture_screenshot(output_path):
    try:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            sct_img = sct.grab(monitor)
            
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            img.save(output_path)
            return True
    except Exception as e:
        print(f"❌ Error capturing screen: {e}")
        return False


def analyze_screenshot(image_path):
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{
                'role': 'user',
                'content': 'Identify the active window or application open and state what task the user is working on in one concise sentence.',
                'images': [image_path]
            }]
        )
        return response['message']['content'].strip()
    except Exception as e:
        return f"Inference Error: {e}"


def main():
    print("🚀 On-Device Productivity Engine Initialized.")
    print(f"Monitoring your primary screen every {CAPTURE_INTERVAL} seconds...")
    print("Logs are updating live. Press Ctrl+C to stop.")
    print("-" * 50)
    
    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if capture_screenshot(TEMP_IMAGE_PATH):
                analysis_text = analyze_screenshot(TEMP_IMAGE_PATH)
                
                with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([timestamp, analysis_text])
                
                print(f"[{timestamp}] Logged: {analysis_text}")
                
                if os.path.exists(TEMP_IMAGE_PATH):
                    os.remove(TEMP_IMAGE_PATH)
                    
            time.sleep(CAPTURE_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n🛑 Background Agent safely terminated.")
        if os.path.exists(TEMP_IMAGE_PATH):
            os.remove(TEMP_IMAGE_PATH)


if __name__ == "__main__":
    main()