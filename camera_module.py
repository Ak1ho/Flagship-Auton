import cv2

class CameraModule:
    def __init__(self, camera_index=0, width=640, height=480):
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.capture = None

    def start(self):
        self.capture = cv2.VideoCapture(self.camera_index)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def get_frame(self):
        if not self.capture:
            return None
        ret, frame = self.capture.read()
        if not ret:
            return None
        return frame
    def release(self):
        if self.capture:
            self.capture.release()
