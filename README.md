# Argus 👁️
Real-time Multi-Camera Object & Animal Detection System

Argus is a Python-based computer vision system designed to analyze **live video streams from multiple cameras** as well as **recorded video files**, detect objects and animals using deep learning models, and log detection events in a scalable and maintainable way.

The project follows **modern Python packaging standards**, uses a clean `src/` layout, and is designed to scale from a **single camera prototype** to a **multi-camera real-time system**.

---

## Features

- Live video analysis from multiple cameras (RTSP / IP cameras / webcam)
- Batch processing of recorded video files
- Object and animal detection using deep learning models (YOLO)
- Real-time inference with configurable FPS limits
- Centralized configuration management
- Structured logging of detection events
- Modular and extensible architecture
- GPU acceleration support (if available)...

---

## Project Structure

```text
argus/
├── README.md
├── pyproject.toml
├── requirements.txt
├── src/
│   └── argus/
│       ├── __init__.py
│       ├── config.py
│       ├── logger.py
│       ├── exceptions.py
│       │
│       ├── streams/
│       │   ├── camera.py
│       │   └── manager.py
│       │
│       ├── detection/
│       │   ├── model.py
│       │   └── infer.py
│       │
│       ├── pipeline/
│       │   ├── worker.py
│       │   └── scheduler.py
│       │
│       └── utils/
│           ├── io.py
│           └── time.py
│
└── tests/