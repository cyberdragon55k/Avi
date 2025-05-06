
# Avi-Automated-Visual-Intelligence

**Avi** 🤖 is an AI-powered system that transforms raw screen recordings into intelligent, classified insights. By integrating FFmpeg, Firebase, and Google Gemini API, Avi automates screen data capture, frame extraction, and AI-based visual analysis — making it easy to understand what was happening on screen, when, and why.

---

## 📚 Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [Architecture & Workflow](#architecture--workflow)  
4. [Technologies Used](#technologies-used)  
5. [Installation & Setup](#installation--setup)  
6. [Usage Guide](#usage-guide)  
7. [Recommendations](#recommendations)  
8. [Contributing](#contributing)  
9. [License](#license)  

---

## 📌 Overview

**Avi (Automated Visual Intelligence)** simplifies the process of monitoring screen usage. It captures screen activity, splits the video into frames, uploads them to Firebase, and analyzes them using Google's **Gemini Vision API**. Finally, it displays the analysis via a **Streamlit dashboard**, giving you a snapshot of what applications or actions were taken over time.

---

## ✨ Features

- 🔴 Screen recording via FFmpeg  
- 🖼️ Frame extraction at set intervals  
- ☁️ Upload frames to Firebase Storage  
- 🧠 Frame classification using Gemini Vision API  
- 📊 Insightful dashboard powered by Streamlit  
- 📝 Activity logging in JSON format  

---

## 🛠 Technologies Used

- **FFmpeg**: Captures desktop screen recordings  
- **Python**: Automates frame extraction, upload, and classification  
- **OpenCV (optional)**: For custom frame manipulation  
- **Firebase**: Stores screenshots and optionally metadata  
- **Google Gemini API**: Provides intelligent image descriptions  
- **Streamlit**: Creates an interactive dashboard to display analysis  

---

## 🔄 Architecture & Workflow

```mermaidgraph TD
  A[Screen Recording (FFmpeg)] --> B[Extract Frames (Python)]
  B --> C[Upload to Firebase Storage]
  C --> D[Classify with Gemini API]
  D --> E[Save to frame_analysis.json]
  E --> F[Visualize in Streamlit Dashboard]


pip install -r requirements.txt