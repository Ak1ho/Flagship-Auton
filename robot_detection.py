import cv2
import numpy as np

class RobotDetector:
    def __init__(self,lower=(0,120,70),upper=(10,255,255)):
        self.lower=np.array(lower,dtype=np.uint8)
        self.upper=np.array(upper,dtype=np.uint8)
    def detect(self,frame):
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        mask=cv2.inRange(hsv,self.lower,self.upper)
        k=np.ones((5,5),np.uint8)
        mask=cv2.erode(mask,k,iterations=1)
        mask=cv2.dilate(mask,k,iterations=2)
        c,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        if c:
            m=max(c,key=cv2.contourArea)
            if cv2.contourArea(m)<100:return None
            x,y,w,h=cv2.boundingRect(m)
            return (x+w//2,y+h//2)
        return None
