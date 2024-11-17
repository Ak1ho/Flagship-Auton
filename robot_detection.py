# robot_detection.py
import cv2
import numpy as np

class RobotDetector:
    def __init__(self):
        self.lower_color = np.array([0, 100, 100])    # Example lower HSV bound
        self.upper_color = np.array([10, 255, 255])   # Example upper HSV bound

    def detect_robot(self, frame):
        # Convert to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create mask based on color range
        mask = cv2.inRange(hsv, self.lower_color, self.upper_color)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Find the largest contour
            c = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(c)
            if area > 500:  # Adjust the area threshold as needed
                # Calculate the center of the contour
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    # Determine direction based on position
                    frame_center = frame.shape[1] / 2
                    direction = 'left' if cX < frame_center else 'right'
                    return True, direction
        return False, None
