import cv2
import logging

class CameraModule:
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.cap = cv2.VideoCapture(camera_id)
        if not self.cap.isOpened():
            logging.error("Failed to open camera with ID %s", camera_id)
            raise ValueError("Camera could not be opened.")

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            logging.error("Failed to capture frame from camera.")
            return None
        return frame

    def release(self):
        if self.cap:
            self.cap.release()
            logging.info("Camera released.")
