import cv2

class CameraModule:
    def __init__(self, camera_index=0, width=640, height=480):
        self.capture = cv2.VideoCapture(camera_index)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        if not self.capture.isOpened():
            raise RuntimeError(f"Could not open camera index {camera_index}")

    def get_frame(self):
        ret, frame = self.capture.read()
        if not ret:
            raise RuntimeError("Failed to read from camera.")
        return frame

    def release(self):
        if self.capture.isOpened():
            self.capture.release()
