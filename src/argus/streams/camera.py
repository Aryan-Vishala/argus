"""
Camera stream reader for Argus.

This module provides a robust Camera class for reading frames
from live video sources such as RTSP streams, IP cameras, or webcams.

Features:
- Automatic reconnect
- FPS throttling
- Safe frame reading
- Structured logging
"""

from __future__ import annotations

import time
import cv2
from typing import Optional

from argus.logger import get_logger
from argus import config
from argus.exceptions import (
    CameraConnectionError,
    CameraReadError,
)


class Camera:
    """
    Represents a single video source (RTSP / IP camera / webcam).
    """

    def __init__(
        self,
        source: str | int,
        *,
        camera_id: Optional[str] = None,
        reconnect_interval: int = config.CAMERA_RECONNECT_INTERVAL,
        target_fps: int = config.TARGET_FPS,
    ) -> None:
        """
        Args:
            source: RTSP URL, video path, or webcam index (0, 1, ...)
            camera_id: Human-readable camera identifier
            reconnect_interval: Seconds between reconnect attempts
            target_fps: FPS throttle (0 disables throttling)
        """

        self.source = source
        self.camera_id = camera_id or str(source)
        self.reconnect_interval = reconnect_interval
        self.target_fps = target_fps

        self._cap: Optional[cv2.VideoCapture] = None
        self._last_frame_time = 0.0
        self._running = False

        self.logger = get_logger(f"argus.camera.{self.camera_id}")

    # -----------------------------
    # Connection management
    # -----------------------------

    def connect(self) -> None:
        """
        Open the camera stream.
        """
        self.logger.info("Connecting to camera")

        cap = cv2.VideoCapture(self.source)
        if not cap.isOpened():
            raise CameraConnectionError(
                f"Unable to open camera source: {self.source}"
            )

        self._cap = cap
        self._running = True
        self.logger.info("Camera connected")

    def disconnect(self) -> None:
        """
        Release the camera resource.
        """
        if self._cap is not None:
            self._cap.release()
            self._cap = None

        self._running = False
        self.logger.info("Camera disconnected")

    def reconnect(self) -> None:
        """
        Attempt to reconnect to the camera.
        """
        self.logger.warning(
            "Reconnecting in %s seconds", self.reconnect_interval
        )
        self.disconnect()
        time.sleep(self.reconnect_interval)
        self.connect()

    # -----------------------------
    # Frame reading
    # -----------------------------

    def read(self):
        """
        Read a single frame from the camera.

        Returns:
            frame (numpy.ndarray)

        Raises:
            CameraReadError
        """
        if not self._cap or not self._running:
            raise CameraReadError("Camera is not connected")

        # FPS throttling
        if self.target_fps > 0:
            min_interval = 1.0 / self.target_fps
            now = time.time()
            elapsed = now - self._last_frame_time
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            self._last_frame_time = time.time()

        success, frame = self._cap.read()

        if not success or frame is None:
            raise CameraReadError("Failed to read frame from camera")

        return frame

    # -----------------------------
    # Streaming loop
    # -----------------------------

    def frames(self):
        """
        Generator yielding frames continuously.

        Automatically reconnects on failure.
        """
        if not self._cap:
            self.connect()

        while self._running:
            try:
                yield self.read()
            except CameraReadError as e:
                self.logger.error(
                    "Camera read failed: %s", e, exc_info=True
                )
                self.reconnect()

    # -----------------------------
    # Context manager support
    # -----------------------------

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.disconnect()
