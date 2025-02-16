"""
robot_detection.py
Module for processing camera frames to detect an opponent robot.
This example uses color-based thresholding as a simple illustration.
Replace or augment with more robust methods (e.g. object detection models).
"""

import cv2
import numpy as np

class OpponentDetector:
    def __init__(self, color_lower=(0, 100, 100), color_upper=(10, 255, 255)):
        """
        color_lower, color_upper: HSV color range for detecting the opponent
        Adjust these values to match the typical color of your opponent if known,
        or use a more generalized detection approach.
        """
        self.color_lower = np.array(color_lower, dtype=np.uint8)
        self.color_upper = np.array(color_upper, dtype=np.uint8)

    def detect_opponent(self, frame):
        """
        Returns the center (x, y) of the detected opponent in the frame,
        along with a detection confidence or bounding box.
        Returns None if not found.
        """
        # Convert to HSV color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Threshold the HSV image to get desired color
        mask = cv2.inRange(hsv_frame, self.color_lower, self.color_upper)

        # Morphological operations to reduce noise
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=2)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) < 100:  # ignore small noise
                return None
            # Get bounding box center
            x, y, w, h = cv2.boundingRect(largest_contour)
            center_x = x + w // 2
            center_y = y + h // 2
            return (center_x, center_y)
        return None
