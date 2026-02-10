import cv2
from argus.detection.infer import run_inference
from argus.utils.visualize import draw_detections
from argus.logger import get_logger


class CameraWorker:
    def __init__(self, camera):
        self.camera = camera
        self.logger = get_logger(f"worker.{camera.camera_id}")

    def run(self):
        self.logger.info("Worker started")

        for frame in self.camera.frames():
            detections = run_inference(frame)
            frame = draw_detections(frame, detections)

            cv2.imshow(self.camera.camera_id, frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.camera.disconnect()
        cv2.destroyAllWindows()
