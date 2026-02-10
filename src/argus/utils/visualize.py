"""
Visualization utilities for Argus.

Responsible only for drawing detections on frames.
No inference, no I/O, no logging side effects.
"""

from __future__ import annotations

import cv2
from typing import List, Dict, Any


def draw_detections(
    frame,
    detections: List[Dict[str, Any]],
    *,
    color=(0, 255, 0),
    thickness=2,
):
    """
    Draw bounding boxes and labels on a frame.

    Args:
        frame: OpenCV image (BGR)
        detections: Output from run_inference
        color: Bounding box color
        thickness: Box thickness
    """
    for det in detections:
        x1, y1, x2, y2 = map(int, det["bbox"])
        label = det["label"]
        conf = det["confidence"]

        text = f"{label} {conf:.2f}"

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
        cv2.putText(
            frame,
            text,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            2,
            cv2.LINE_AA,
        )

    return frame
