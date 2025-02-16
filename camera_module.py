import cv2

class CameraModule:
    def __init__(self,index=0):
        self.cap=cv2.VideoCapture(index)
    def read_frame(self):
        ret,frame=self.cap.read()
        if not ret:return None
        return frame
    def release(self):
        self.cap.release()
