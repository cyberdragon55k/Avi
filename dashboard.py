import streamlit as st
import json
from PIL import Image
import os

st.set_page_config(page_title="Screen Activity Dashboard", layout="wide")

st.title("📊 Screen Activity Dashboard")

ANALYSIS_FILE = "frame_analysis.json"
OUTPUT_DIR = "screenshots"

if not os.path.exists(ANALYSIS_FILE):
    st.warning("No analysis found. Run `screen_analyzer.py` first.")
    st.stop()

with open(ANALYSIS_FILE, "r") as f:
    data = json.load(f)

app_summary = {}
st.markdown("### Frame Insights")

for item in data:
    col1, col2 = st.columns([1, 2])
    image_path = os.path.join(OUTPUT_DIR, item["frame"])
    description = item["description"]

    # Attempt to infer app from description
    app = "Unknown"
    if "YouTube" in description:
        app = "YouTube"
    elif "Chrome" in description or "browser" in description:
        app = "Browser"
    elif "code" in description or "editor" in description:
        app = "Code Editor"
    elif "PowerPoint" in description:
        app = "PowerPoint"
    elif "game" in description:
        app = "Game"

    app_summary[app] = app_summary.get(app, 0) + 1

    with col1:
        st.image(Image.open(image_path), caption=item["frame"], use_column_width=True)
    with col2:
        st.markdown(f"**Timestamp**: {item['timestamp']}")
        st.markdown(f"**Analysis**: {description}")
        st.markdown(f"**Detected App**: `{app}`")

# Show summary
st.markdown("## 📈 App Usage Summary")
st.bar_chart(app_summary)
