<![CDATA[<div align="center">

# 🏋️‍♂️ Real-time GYM Coach

**AI-Powered Personal Trainer with Live Pose Detection & Voice Coaching**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.54-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-4285F4?logo=google&logoColor=white)](https://mediapipe.dev)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F55036)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A full-stack, browser-based fitness application that uses your webcam to detect exercise form in real time, count reps and sets automatically, and deliver proactive AI voice coaching — all running locally through a Streamlit interface.

</div>

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Supported Exercises](#-supported-exercises)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Architecture](#-architecture)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the App](#running-the-app)
- [Module Breakdown](#-module-breakdown)
  - [Core](#core)
  - [Detectors](#detectors)
  - [Services](#services)
- [How It Works](#-how-it-works)
- [Configuration](#-configuration)
- [Database Schema](#-database-schema)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔭 Overview

**Real-time GYM Coach** is an AI-powered personal trainer that transforms your webcam into a smart fitness companion. It uses **MediaPipe Pose Landmarker** to track 33 body keypoints in real time, runs exercise-specific detection algorithms to count reps, evaluate form, and track sets — then uses a **Groq-hosted LLaMA 3.3 70B** model to generate context-aware coaching cues that are spoken aloud via **Google Text-to-Speech (gTTS)**.

The entire application runs in the browser through **Streamlit** with **WebRTC** for low-latency video streaming — no additional hardware or mobile app required.

---

## ✨ Key Features

| Category | Feature |
|---|---|
| **Pose Detection** | Real-time 33-keypoint body tracking via MediaPipe Pose Landmarker (full model) |
| **Exercise Analysis** | Automatic rep counting with up/down state machine logic |
| **Form Evaluation** | Joint angle calculation, depth checks, body alignment, swing detection, and balance analysis |
| **AI Voice Coaching** | Proactive spoken feedback powered by LLaMA 3.3 70B (Groq) + gTTS |
| **Workout Planning** | Configurable exercise, sets, and reps per session |
| **Progress Tracking** | Automatic set completion detection and workout history stored in SQLite |
| **User Accounts** | Simple username-based login with persistent workout history |
| **Live Overlays** | Skeleton rendering and exercise-specific status overlays on the video feed |
| **Dark Theme UI** | Custom-styled dark interface with Adobe Clean typography |

---

## 💪 Supported Exercises

Each exercise has a dedicated detector with tailored form metrics:

| Exercise | Metrics Tracked | Form Checks |
|---|---|---|
| **Squats** | Knee Angle, Back Angle | Depth status (Good Depth / Too High), forward lean detection |
| **Push-ups** | Elbow Angle | Body alignment (Straight / Slight Bend / Poor Form), hip position (Level / Sagging / Piked) |
| **Biceps Curls** | Elbow Angle | Shoulder stability (Stable / Elbow Drifting), swing detection (No Swing / Swinging) |
| **Shoulder Press** | Elbow Angle | Arm extension status, back arch detection (Neutral / Slight / Excessive) |
| **Lunges** | Front Knee Angle, Torso Angle | Balance status (Balanced / Off Balance), lateral offset check |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | [Streamlit](https://streamlit.io) 1.54 | Web UI framework |
| **Video Streaming** | [streamlit-webrtc](https://github.com/whitphx/streamlit-webrtc) 0.64 | Real-time webcam via WebRTC |
| **Pose Estimation** | [MediaPipe](https://mediapipe.dev) 0.10 | Full-body pose landmark detection |
| **Computer Vision** | [OpenCV](https://opencv.org) 4.10 | Frame processing, skeleton drawing |
| **LLM** | [Groq](https://groq.com) (LLaMA 3.3 70B) | AI coaching feedback generation |
| **Text-to-Speech** | [gTTS](https://gtts.readthedocs.io) 2.5 | Voice audio synthesis |
| **Database** | SQLite 3 | User accounts and workout history |
| **Data Processing** | [Pandas](https://pandas.pydata.org) 2.2 | Workout history aggregation |
| **Config** | [python-dotenv](https://github.com/theskumar/python-dotenv) | Environment variable management |

---

## 📁 Project Structure

```
Gym Coach/
├── .env                          # Environment variables (API keys)
├── .gitignore                    # Git ignore rules
├── .streamlit/
│   └── config.toml               # Streamlit theme configuration
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
├── data.db                       # SQLite database (auto-created)
│
├── core/
│   └── base_exercise.py          # Abstract base class for all exercise detectors
│
├── detectors/
│   ├── biceps_curl.py            # Biceps curl detection & form analysis
│   ├── lunges.py                 # Lunge detection & balance tracking
│   ├── pushup.py                 # Push-up detection & alignment analysis
│   ├── shoulder_press.py         # Shoulder press detection & arch monitoring
│   └── squat.py                  # Squat detection & depth evaluation
│
├── ml_models/
│   └── pose_landmarker_full.task # MediaPipe Pose Landmarker model (~9 MB)
│
├── services/
│   ├── auth/
│   │   └── login_wall.py         # Username-based authentication gate
│   ├── coaching/
│   │   ├── llm.py                # LLM coach (Groq API wrapper)
│   │   ├── tts.py                # Text-to-Speech (gTTS wrapper)
│   │   └── voice_pipeline.py     # Orchestrates LLM → TTS → audio playback
│   ├── config/
│   │   └── workout_config.py     # Exercise options, pose connections, LLM prompt
│   ├── persistence/
│   │   └── exercise_repository.py# SQLite CRUD for users and exercises
│   ├── state/
│   │   └── session_defaults.py   # Streamlit session state initialization
│   ├── tracking/
│   │   └── metrics.py            # Real-time metrics sync & voice trigger logic
│   ├── ui/
│   │   ├── style_loader.py       # CSS/font injection & WebRTC style patching
│   │   └── AdobeClean.otf        # Custom font file
│   └── vision/
│       └── exercise_video_processor.py # WebRTC video processor (pose + detectors)
│
└── static/
    └── style.css                 # Global application styles (dark theme)
```

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        BROWSER (Streamlit UI)                    │
│  ┌──────────┐  ┌───────────────┐  ┌───────────────────────────┐ │
│  │  Sidebar  │  │  Video Feed   │  │    Workout History Table  │ │
│  │  ─────── │  │  (WebRTC)     │  │    (Pandas DataFrame)     │ │
│  │ Exercise  │  │  + Skeleton   │  └───────────────────────────┘ │
│  │ Sets/Reps │  │  + Overlays   │                                │
│  │ Progress  │  └──────┬────────┘  ┌───────────────────────────┐ │
│  │ Metrics   │         │           │  🔊 Coach Feedback (TTS)  │ │
│  └──────────┘         │           └───────────────────────────┘ │
└───────────────────────┼──────────────────────────────────────────┘
                        │
          ┌─────────────▼──────────────┐
          │   VideoProcessorClass      │
          │   (streamlit-webrtc)       │
          │                            │
          │  ┌────────────────────┐    │
          │  │  MediaPipe Pose    │    │
          │  │  Landmarker (Full) │    │
          │  └────────┬───────────┘    │
          │           │ landmarks      │
          │  ┌────────▼───────────┐    │
          │  │  Exercise Detector │    │
          │  │  (Squat/Pushup/…) │    │
          │  └────────┬───────────┘    │
          │           │ metrics        │
          └───────────┼────────────────┘
                      │
          ┌───────────▼────────────────┐
          │   Metrics Sync Layer       │
          │   (tracking/metrics.py)    │
          │                            │
          │   • Rep / Set counting     │
          │   • Session state updates  │
          │   • DB persistence         │
          │   • Voice trigger logic    │
          └───────────┬────────────────┘
                      │
          ┌───────────▼────────────────┐
          │   Voice Pipeline           │
          │                            │
          │  ┌──────────────────────┐  │
          │  │  Form Issue Detector │  │
          │  └──────────┬───────────┘  │
          │             │              │
          │  ┌──────────▼───────────┐  │
          │  │  LLM Coach (Groq)   │  │
          │  │  LLaMA 3.3 70B      │  │
          │  └──────────┬───────────┘  │
          │             │ text         │
          │  ┌──────────▼───────────┐  │
          │  │  TTS (gTTS)         │  │
          │  │  → MP3 audio bytes  │  │
          │  └─────────────────────┘  │
          └────────────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** installed on your system
- **Webcam** accessible from the browser
- **Groq API Key** — get one free at [console.groq.com](https://console.groq.com)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Aryan2005-tech/Real-time_GYM-Coach.git
   cd Real-time_GYM-Coach
   ```

2. **Create and activate a virtual environment**

   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS / Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download the MediaPipe model** (if not included)

   The app expects the model file at `ml_models/pose_landmarker_full.task`. If it is not present, download it from the [MediaPipe model page](https://developers.google.com/mediapipe/solutions/vision/pose_landmarker#models).

### Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY="your_groq_api_key_here"
```

> **Note:** The API key can also be set in `.streamlit/secrets.toml` as `GROQ_API_KEY` for Streamlit Cloud deployments.

### Running the App

```bash
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 📦 Module Breakdown

### Core

#### [`base_exercise.py`](core/base_exercise.py)

Abstract base class that all exercise detectors inherit from. Provides:

- **`calculate_angle(a, b, c)`** — Computes the angle at point `b` formed by points `a`, `b`, `c` using the dot-product formula. Returns degrees (0°–180°).
- **`get_point(landmarks, idx)`** — Extracts `(x, y)` coordinates from a MediaPipe landmark by index.
- **`process(landmarks)`** — Abstract method; each detector implements its own rep-counting and form-analysis logic.
- **`reset()`** — Abstract method; resets rep count and internal state.

---

### Detectors

Each detector follows the same pattern: analyze landmarks → count reps via a state machine → return a metrics dictionary.

| Detector | State Machine | Key Angles |
|---|---|---|
| **SquatDetector** | `down` (knee < 100°) → `up` (knee ≥ 160°) = 1 rep | Knee angle, back angle |
| **PushUpDetector** | `down` (elbow < 90°) → `up` (elbow > 160°) = 1 rep | Elbow angle, body angle |
| **BicepsCurlDetector** | `up` (elbow < 50°) → `down` (elbow > 160°) = 1 rep | Elbow angle, torso angle |
| **ShoulderPressDetector** | `up` (elbow > 160°) → `down` (elbow < 90°) = 1 rep | Elbow angle, back angle |
| **LungesDetector** | `down` (knee < 100°) → `up` (knee > 160°) = 1 rep | Front knee angle, torso angle |

All detectors automatically select the more visible side (left vs. right) using landmark visibility scores.

---

### Services

#### 🔐 Auth — [`login_wall.py`](services/auth/login_wall.py)

Renders a simple username form that gates the entire app. Users are created in SQLite on first login, and subsequent logins retrieve the existing record. The `user_id` is stored in `st.session_state` for the session duration.

#### 🤖 Coaching

| File | Description |
|---|---|
| [`llm.py`](services/coaching/llm.py) | Wraps the Groq API. Sends a system prompt + conversation history (last 10 messages) to **LLaMA 3.3 70B Versatile** at temperature 0.4. Returns short, motivational coaching cues. |
| [`tts.py`](services/coaching/tts.py) | Converts text to MP3 audio bytes using Google TTS (`gTTS`). |
| [`voice_pipeline.py`](services/coaching/voice_pipeline.py) | Orchestrates the full feedback loop: **detect form issue → LLM → TTS → audio playback**. Includes a 5-second cooldown between non-critical voice cues to avoid spamming. Also contains the `autoplay_audio()` helper that injects an HTML `<script>` to play audio in the parent window. |

#### ⚙️ Config — [`workout_config.py`](services/config/workout_config.py)

Central configuration file containing:
- `EXERCISE_OPTIONS` — List of supported exercise names.
- `POSE_CONNECTIONS` — MediaPipe landmark index pairs for skeleton drawing.
- `METRICS_FIELDS` — Default metric keys and values per exercise (used for session state initialization).
- `PROMPT` — The full system prompt for the LLM coach persona ("Apna AI Coach").

#### 💾 Persistence — [`exercise_repository.py`](services/persistence/exercise_repository.py)

SQLite data access layer with the following operations:
- `init_db()` — Creates `users` and `exercises` tables if they don't exist.
- `get_or_create_user(username)` — Upsert-style user lookup.
- `add_exercise(user_id, name, reps, sets, time)` — Inserts or updates (accumulates) exercise records for the current day.
- `get_users_exercises(user_id)` — Retrieves all exercise history for a user.

#### 📊 State — [`session_defaults.py`](services/state/session_defaults.py)

Initializes all Streamlit `session_state` keys with sensible defaults (angles at 0, statuses at "N/A", flags at `False`, etc.) to prevent `KeyError` on first render.

#### 📈 Tracking — [`metrics.py`](services/tracking/metrics.py)

The real-time synchronization engine that bridges the WebRTC video processor and the Streamlit UI:
1. Reads latest metrics from the video processor thread.
2. Updates session state with current angles, statuses, and rep counts.
3. Calculates sets completed and detects workout completion.
4. Persists completed sets to the database.
5. Triggers voice coaching events (`set_completed`, `workout_completed`, `no_pose_detected`, `ongoing_form_check`) via background threads.

#### 🎨 UI — [`style_loader.py`](services/ui/style_loader.py)

Handles all visual customization:
- `load_css()` — Injects the global `style.css` into the Streamlit page.
- `inject_local_font()` — Base64-encodes and injects the Adobe Clean font as a `@font-face` rule.
- `inject_webrtc_styles()` — Patches the WebRTC iframe's internal stylesheet to apply custom fonts and remove border-radius from MUI buttons.

#### 👁️ Vision — [`exercise_video_processor.py`](services/vision/exercise_video_processor.py)

The core video processing pipeline running on the WebRTC thread:
1. Receives each video frame via `recv()`.
2. Flips the frame horizontally (mirror mode).
3. Runs MediaPipe Pose Landmarker in `VIDEO` mode.
4. Draws the skeleton (green lines, blue dots) on detected landmarks.
5. Routes landmarks to the active exercise detector.
6. Draws exercise-specific status overlays on the frame.
7. Stores the latest metrics in a thread-safe dictionary for the UI to poll.

---

## ⚙️ How It Works

```
1. User logs in  →  Username stored in session + SQLite
2. User configures workout  →  Exercise type, sets, reps
3. User clicks "Start Workout"  →  WebRTC camera activates
4. Each video frame:
   a. MediaPipe detects 33 body keypoints
   b. Exercise detector calculates joint angles
   c. State machine counts reps (up/down transitions)
   d. Metrics written to thread-safe shared memory
5. Streamlit main thread (every 250ms):
   a. Reads latest metrics from video processor
   b. Updates sidebar progress (reps, sets, angles)
   c. Checks for set completion → saves to DB
   d. Triggers voice coaching on events/form issues
6. Voice Pipeline (background thread):
   a. Detects form issues from metrics
   b. Sends event + issue to LLM for coaching text
   c. Converts text to audio via gTTS
   d. Audio auto-played in browser
7. User clicks "End Workout"  →  Camera stops, summary shown
```

---

## 🎛️ Configuration

### Streamlit Theme (`.streamlit/config.toml`)

```toml
[theme]
primaryColor = "#444444"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#1E232B"
textColor = "#FFFFFF"
```

### Exercise Detector Thresholds

Each detector has configurable constants at the class level:

| Detector | Constant | Default | Description |
|---|---|---|---|
| Squat | `DOWN_THRESHOLD` | 100° | Knee angle below which a squat is "down" |
| Squat | `UP_THRESHOLD` | 160° | Knee angle above which a squat is "up" |
| Push-up | `DOWN_THRESHOLD` | 90° | Elbow angle below which a push-up is "down" |
| Push-up | `HIP_SAG_TOLERANCE` | 0.08 | Max hip deviation before "Sagging" warning |
| Biceps Curl | `UP_THRESHOLD` | 50° | Elbow angle below which a curl is "up" |
| Biceps Curl | `SWING_THRESHOLD` | 15° | Torso lean angle triggering "Swinging" warning |
| Shoulder Press | `UP_THRESHOLD` | 160° | Elbow angle above which the press is "up" |
| Lunges | `BALANCE_TOLERANCE` | 0.10 | Max lateral offset before "Off Balance" warning |

All detectors use a **minimum landmark visibility** of `0.7` to ensure reliable detection.

### Voice Pipeline

| Setting | Value | Description |
|---|---|---|
| Cooldown | 5 seconds | Minimum interval between non-critical voice cues |
| LLM Model | `llama-3.3-70b-versatile` | Groq-hosted model for coaching text |
| LLM Temperature | 0.4 | Controls creativity of coaching responses |
| History Window | Last 10 messages | Conversation context sent to the LLM |

---

## 🗄️ Database Schema

The application uses a local SQLite database (`data.db`) with two tables:

### `users`

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER (PK) | Auto-incrementing user ID |
| `username` | TEXT (UNIQUE) | User's display name |
| `created_at` | TIMESTAMP | Account creation time |

### `exercises`

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER (PK) | Auto-incrementing record ID |
| `user_id` | INTEGER (FK → users) | Reference to the user |
| `exercise_name` | TEXT | Name of the exercise performed |
| `reps` | INTEGER | Total reps (accumulated per day) |
| `sets` | INTEGER | Total sets (accumulated per day) |
| `time` | INTEGER | Total time in seconds |
| `created_at` | TIMESTAMP | Record creation time |

---

## 🖼️ Screenshots

> _Screenshots will be added here. Run the app and capture the login screen, active workout view with skeleton overlay, sidebar metrics, and workout history table._

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/new-exercise`)
3. **Commit** your changes (`git commit -m 'Add deadlift detector'`)
4. **Push** to the branch (`git push origin feature/new-exercise`)
5. **Open** a Pull Request

### Adding a New Exercise

1. Create a new detector class in `detectors/` extending `BaseExercise`.
2. Implement `process(landmarks)` with your rep-counting state machine.
3. Add the exercise name to `EXERCISE_OPTIONS` in `workout_config.py`.
4. Add default metrics to `METRICS_FIELDS` in `workout_config.py`.
5. Add session state defaults in `session_defaults.py`.
6. Add UI metrics display in the sidebar section of `main.py`.
7. Add form issue detection in `voice_pipeline.py` → `_find_form_issue()`.
8. Register the detector in `exercise_video_processor.py` → `_detectors` dict.
9. Add overlay drawing method in `exercise_video_processor.py`.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

**Built with ❤️ using Streamlit, MediaPipe, and Groq**

</div>
]]>
