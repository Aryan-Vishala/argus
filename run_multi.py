import threading

from argus.streams.manager import CameraManager
from argus.pipeline.worker import CameraWorker


def run_worker(worker: CameraWorker):
    worker.run()


manager = CameraManager()
manager.load_cameras()

threads = []

for cam in manager.get_cameras():
    worker = CameraWorker(cam)
    t = threading.Thread(
        target=run_worker,
        args=(worker,),
        daemon=True,
    )
    threads.append(t)
    t.start()

# Keep main thread alive
try:
    for t in threads:
        t.join()
except KeyboardInterrupt:
    print("Shutting down...")
