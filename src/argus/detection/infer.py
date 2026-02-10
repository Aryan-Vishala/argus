"""
Inference utilities for Argus.

This module contains logic for running object detection
on frames using the shared DetectionModel.
"""

from __future__ import annotations

from typing import List, Dict, Any

import numpy as np

from argus.detection.model import DetectionModel
from argus.logger import get_logger
from argus import config
from argus.exceptions import InferenceError

logger = get_logger(__name__)


def run_inference(
    frame: np.ndarray,
    *,
    confidence_threshold: float = config.CONFIDENCE_THRESHOLD,
) -> List[Dict[str, Any]]:
    """
    Run object detection on a single frame.

    Args:
        frame: Image frame (BGR, OpenCV format)
        confidence_threshold: Minimum confidence score

    Returns:
        List of detection dictionaries
    """
    try:
        model = DetectionModel.load()

        results = model(frame, verbose=False)

        detections: List[Dict[str, Any]] = []

        for r in results:
            if r.boxes is None:
                continue

            for box in r.boxes:
                conf = float(box.conf[0])
                if conf < confidence_threshold:
                    continue

                cls_id = int(box.cls[0])
                label = r.names.get(cls_id, str(cls_id))

                x1, y1, x2, y2 = map(float, box.xyxy[0])

                detections.append(
                    {
                        "label": label,
                        "confidence": conf,
                        "bbox": [x1, y1, x2, y2],
                    }
                )

        return detections

    except Exception as e:
        logger.error("Inference failed", exc_info=True)
        raise InferenceError(str(e))
