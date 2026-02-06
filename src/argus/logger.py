"""
Centralized logging configuration for Argus.
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
import sys
from pathlib import Path
from typing import Optional

from argus import config


# -----------------------------
# Internal helper
# -----------------------------

def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


# -----------------------------
# Public API
# -----------------------------

def get_logger(
    name: str,
    *,
    level: Optional[int] = None,
) -> logging.Logger:
    """
    Get a configured logger instance.

    This function is safe to call multiple times with the same name.
    """

    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    level = level or config.LOG_LEVEL
    logger.setLevel(level)
    logger.propagate = False

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # -----------------------------
    # Console handler
    # -----------------------------
    if config.LOG_TO_CONSOLE:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # -----------------------------
    # File handler
    # -----------------------------
    if config.LOG_TO_FILE:
        _ensure_dir(config.LOG_DIR)
        file_path = config.LOG_DIR / config.LOG_FILE_NAME

        file_handler = RotatingFileHandler(
            filename=file_path,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
