"""
Central configuration for Argus.

This module defines all system-wide configuration values.
No business logic should live here.
"""

from __future__ import annotations

from pathlib import Path
import logging
import os


# -----------------------------
# Project paths
# -----------------------------

# Root of the project (…/argus)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
VIDEO_DIR = DATA_DIR / "videos"

OUTPUT_DIR = PROJECT_ROOT / "outputs"
LOG_DIR = OUTPUT_DIR / "logs"


# -----------------------------
# Logging configuration
# -----------------------------

LOG_LEVEL = logging.INFO
LOG_FILE_NAME = "argus.log"

LOG_TO_CONSOLE = True
LOG_TO_FILE = True


# -----------------------------
# Detection / ML settings
# -----------------------------

CONFIDENCE_THRESHOLD = 0.4
IOU_THRESHOLD = 0.5

INFERENCE_BATCH_SIZE = 8
TARGET_FPS = 10


# -----------------------------
# Live camera settings
# -----------------------------

MAX_CAMERAS = 16
FRAME_QUEUE_SIZE = 10
CAMERA_RECONNECT_INTERVAL = 3  # seconds
RTSP_TIMEOUT = 5  # seconds


# -----------------------------
# Environment overrides (optional)
# -----------------------------

def _get_env_log_level(default: int) -> int:
    level = os.getenv("ARGUS_LOG_LEVEL")
    if not level:
        return default
    return getattr(logging, level.upper(), default)


LOG_LEVEL = _get_env_log_level(LOG_LEVEL)
