# Hand Gesture Recognition using OpenCV & MediaPipe

### NOTE
This README file was generated with the help of AI.
For the original, unedited notes, see `Notes.txt`.

This is a learning project that detects hand gestures in real time and performs actions based on them (executing system commands).

The project uses:
- OpenCV for video capture and visualization
- MediaPipe for hand tracking and gesture recognition

I also fine-tuned a MediaPipe gesture model to go beyond the limited default gestures.

This project is not meant to be production-ready.  
It is meant to understand how things work, line by line.

---

## What This Project Does

- Captures video from a camera
- Detects a hand and its landmarks
- Recognizes gestures
- Applies buffering and cooldown logic to avoid repeated triggers
- Executes actions only when a gesture is stable

Important concept:

Gestures are detected per frame, not per second.  
Without filtering, one gesture could trigger an action dozens of times per second.

---

## Default vs Custom Gestures

### Default MediaPipe gestures (7)

- Closed_Fist  
- Open_Palm  
- Pointing_Up  
- Thumb_Down  
- Thumb_Up  
- Victory  
- ILoveYou  

These were too limited for experimentation.

---

### Custom Fine-Tuned Gestures (20)

Closed_Fist, call, 
dislike, fist, four  
like, mute, ok  
one, palm, peace  
peace_inverted, rock, stop  
stop_inverted, three, three2  
two_up, two_up_inverted  

Gesture names come directly from dataset folder names.

---

## Very Important Notes

### MediaPipe Version Mismatch

Most tutorials and docs online use older MediaPipe APIs.

In this project:
- main.py uses the new MediaPipe API
- training.py uses MediaPipe Model Maker (older API)

They cannot run in the same Python environment.

---

### Separate Virtual Environments (Required)

You must use two virtual environments to avoid dependency conflicts.

#### Runtime Environment (main.py)

```bash
python -m venv venv-runtime
source venv-runtime/bin/activate
pip install mediapipe opencv-python
```

#### Training Environment (training.py)
- Use it with Python version 3.10.13

```bash
python -m venv venv-training
source venv-training/bin/activate
pip install mediapipe_model_maker
```

MediaPipe Model Maker will download all required dependencies automatically.

---

## Dataset Setup

### Starting Point (Kaggle)

Dataset source (thanks to Kaggle and contributors):
https://www.kaggle.com/datasets/innominate817/hagrid-sample-30k-384p/data

---

### Dataset Rules

- You only need the directory that contains subfolders with images
- Each subfolder name becomes a gesture label
- Folder name = gesture name

Example:
```
fist/
like/
peace/
```

---

### Missing no_gesture Class

The dataset does not include a no_gesture class.

Without it, the model tends to hallucinate gestures.

To fix this:

```bash
python3 download.py -d -t no_gesture
```

Then:
1. Rename the folder to no_gesture
2. Add it to the dataset
3. Remove hidden files or directories

download.py source (thanks to them):
https://github.com/hukenovs/hagrid/blob/master/download.py

---

## Fine-Tuning the Model

Based on documentation and research:
- Aim for around 100 samples per gesture

Official documentation:
https://ai.google.dev/edge/mediapipe/solutions/customization/gesture_recognizer

---

### Training Notes

- training.py is ready to use
- Single-hand training only
- Dataset path is local (adjust as needed)
- Use Google Colab if hardware is limited

---

## Python Version (Training)

- Python version used: 3.10.13
- Recommended tool: pyenv

Required library:
mediapipe_model_maker==0.2.1.4

TensorFlow warnings are normal. CPU fallback is expected.

---

## Installing Python 3.10.13 with pyenv (Arch Linux Example)

```bash
sudo pacman -S --needed base-devel libffi zlib xz bzip2 sqlite tk
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

Add to shell:

```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
```

Install Python:

```bash
pyenv install 3.10.13
pyenv local 3.10.13
```

---

## Gesture Logic

This project implements:
- Frame buffering (gesture must appear multiple times)
- Confidence threshold
- Cooldown timing

This prevents command spam and accidental triggers.

---

## Extending the Project

Possible extensions:
- Use landmark coordinates for scrolling or zooming
- Add visual HUD overlays (volume level, state)
- Map gestures to media or system controls
- Combine gestures with motion (direction, speed)

---

## Useful Links

OpenCV:
https://docs.opencv.org/4.12.0/dd/d43/tutorial_py_video_display.html

MediaPipe:
https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer/python#video  
https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker  
https://ai.google.dev/edge/mediapipe/solutions/customization/gesture_recognizer  

---

## Challenges & Reflection

This project was challenging because:
- First time using OpenCV
- First time using MediaPipe
- First time fine-tuning a model

But it was one of the most educational projects I have worked on.

Notes:
- AI tools (ChatGPT and Perplexity) helped a lot
- Code was not copy-pasted
- Every line was understood before being written
