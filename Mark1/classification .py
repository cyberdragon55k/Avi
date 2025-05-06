import os
import base64
import requests
import streamlit as st
from PIL import Image


# === CONFIG ===
API_KEY = "AIzaSyCNC7o8jOGZzBdb7KHKHBQOj29qwpJg7OI"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def classify_image(image_path):
    base64_img = encode_image_to_base64(image_path)
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

    response = requests.post(GEMINI_API_URL, headers=HEADERS, json=payload)
    if response.ok:
        try:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        except KeyError:
            return "No classification result."
    else:
        return f"Error: {response.status_code} - {response.text}"

# === DASHBOARD ===
st.set_page_config(page_title="Gemini PNG Classifier", layout="wide")
st.title("🧠 Gemini Vision - PNG Classifier")

png_folder = "screenshots"
png_files = [f for f in os.listdir(png_folder) if f.lower().endswith(".png")]

if not png_files:
    st.warning("No PNG files found in the 'screenshots' folder.")
else:
    for filename in png_files:
        full_path = os.path.join(png_folder, filename)
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(Image.open(full_path), caption=filename, width=250)
        with col2:
            with st.spinner(f"Classifying {filename}..."):
                result = classify_image(full_path)
                st.success(result)
