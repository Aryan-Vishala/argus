"""
Model loader for Argus.

Loads the detection model once and provides a shared interface
for inference across the system.
"""

from __future__ import annotations

import torch
from ultralytics import YOLO

from argus.logger import get_logger
from argus.exceptions import ModelLoadError

logger = get_logger(__name__)


class DetectionModel:
    """
    Singleton-style wrapper for YOLO model.
    """

    _model = None
    _device = None

    @classmethod
    def load(
        cls,
        weights: str = "yolov8n.pt",
        device: str | None = None,
    ):
        """
        Load the detection model if not already loaded.

        Args:
            weights: Path or name of YOLO weights
            device: 'cpu', 'cuda', or None (auto)
        """
        if cls._model is not None:
            return cls._model

        try:
            cls._device = device or (
                "cuda" if torch.cuda.is_available() else "cpu"
            )

            logger.info(
                "Loading model %s on device %s", weights, cls._device
            )

            cls._model = YOLO(weights)
            cls._model.to(cls._device)

            logger.info("Model loaded successfully")

            return cls._model

        except Exception as e:
            logger.error("Failed to load model", exc_info=True)
            raise ModelLoadError(str(e))
