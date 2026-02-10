from argus.streams.camera import Camera
from argus import config
from argus.logger import get_logger

logger = get_logger(__name__)


class CameraManager:
    def __init__(self):
        self.cameras = []

    def load_cameras(self):
        for cam_cfg in config.CAMERA_SOURCES:
            cam = Camera(
                cam_cfg["source"],
                camera_id=cam_cfg["id"],
            )
            self.cameras.append(cam)

        logger.info("Loaded %d cameras", len(self.cameras))

    def get_cameras(self):
        return self.cameras
