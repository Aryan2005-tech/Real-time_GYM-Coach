# 🏋️ Real-Time GYM Coach

### AI-Powered Personal Trainer with Real-Time Pose Detection and Voice Coaching

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python">
  <img src="https://img.shields.io/badge/Streamlit-Web_App-red?logo=streamlit">
  <img src="https://img.shields.io/badge/MediaPipe-Pose_Detection-green">
  <img src="https://img.shields.io/badge/Groq-Llama_3.3_70B-orange">
</p>

---

## 📌 Overview

Real-Time GYM Coach is an AI-powered fitness assistant that transforms a webcam into a smart personal trainer.

Using computer vision and large language models, the application can:

* Detect body posture in real time
* Count repetitions automatically
* Analyze exercise form
* Track workout progress
* Generate personalized voice feedback
* Store workout history locally

The system combines **MediaPipe Pose Detection**, **OpenCV**, **Streamlit**, and **Llama 3.3 70B (Groq)** to provide an interactive workout experience directly in the browser.

---

## ✨ Key Features

### 🎯 Real-Time Pose Tracking

* 33-body landmark detection using MediaPipe
* Live skeleton visualization
* Real-time movement analysis

### 📊 Smart Workout Tracking

* Automatic rep counting
* Set completion detection
* Progress monitoring

### 🧠 Form Analysis

* Joint angle calculations
* Posture validation
* Balance and alignment checks
* Exercise-specific feedback

### 🎙️ AI Voice Coach

* Context-aware workout guidance
* Form correction suggestions
* Motivational coaching cues
* Voice responses generated using Llama 3.3 70B + gTTS

### 💾 Workout History

* User workout tracking
* Persistent storage with SQLite
* Historical workout records

---

## 💪 Supported Exercises

| Exercise       | Metrics Tracked              |
| -------------- | ---------------------------- |
| Squats         | Knee Angle, Back Angle       |
| Push-Ups       | Elbow Angle, Body Alignment  |
| Biceps Curls   | Elbow Angle, Swing Detection |
| Shoulder Press | Arm Extension, Back Arch     |
| Lunges         | Knee Angle, Balance Analysis |

---

## 🏗️ System Architecture

```text
Webcam
   │
   ▼
MediaPipe Pose Detection
   │
   ▼
Exercise Detector
   │
   ├── Rep Counting
   ├── Form Analysis
   └── Metrics Extraction
   │
   ▼
Tracking Engine
   │
   ├── Streamlit Dashboard
   ├── SQLite Database
   └── AI Voice Coach
              │
              ▼
       Llama 3.3 70B (Groq)
              │
              ▼
            gTTS
```

---

## 🛠️ Tech Stack

| Category            | Technology           |
| ------------------- | -------------------- |
| Frontend            | Streamlit            |
| Computer Vision     | OpenCV               |
| Pose Estimation     | MediaPipe            |
| Real-Time Streaming | streamlit-webrtc     |
| LLM                 | Groq (Llama 3.3 70B) |
| Text-to-Speech      | gTTS                 |
| Database            | SQLite               |
| Data Processing     | Pandas               |

---

## 📂 Project Structure

```text
Real-time_GYM-Coach
│
├── core/
├── detectors/
├── services/
│   ├── auth/
│   ├── coaching/
│   ├── persistence/
│   ├── tracking/
│   ├── ui/
│   └── vision/
│
├── ml_models/
├── static/
├── main.py
└── requirements.txt
```

---

## 🚀 Running the Project

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key
```

Start the application:

```bash
streamlit run main.py
```

Open:

```text
http://localhost:8501
```

---

## ⚙️ Workflow

1. User selects an exercise and workout target.
2. Webcam feed is processed in real time.
3. MediaPipe extracts body landmarks.
4. Exercise-specific detectors analyze movement.
5. Repetitions and sets are counted automatically.
6. Form issues are identified.
7. AI coach generates personalized feedback.
8. Voice responses are played to the user.
9. Workout history is stored in SQLite.

---

## 📸 Screenshots

### Login Screen

*Add screenshot here*

### Live Pose Detection

*Add screenshot here*

### Workout Dashboard

*Add screenshot here*

### Progress Tracking

*Add screenshot here*

---

## 🔮 Future Improvements

* Additional exercise support
* Personalized workout plans
* Performance analytics dashboard
* Mobile-friendly deployment
* Multi-user support

---


---

<p align="center">
Built with ❤️ using Streamlit, MediaPipe, OpenCV, and Groq
</p>
