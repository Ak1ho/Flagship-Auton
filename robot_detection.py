import cv2
import numpy as np
import logging

class RobotDetector:
    def __init__(self):
        # Set HSV color range for detecting the opponent.
        # This example uses a red color range; adjust these values based on your opponent’s appearance.
        self.lower_hsv = np.array([0, 120, 70])
        self.upper_hsv = np.array([10, 255, 255])
        # To also capture upper red hues, you might add:
        self.lower_hsv2 = np.array([170, 120, 70])
        self.upper_hsv2 = np.array([180, 255, 255])

    def detect_opponent(self, frame):
        """Detects the opponent in the frame.
        
        Returns the (x, y) coordinates of the target’s center if found, else None.
        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Create masks for red color
        mask1 = cv2.inRange(hsv, self.lower_hsv, self.upper_hsv)
        mask2 = cv2.inRange(hsv, self.lower_hsv2, self.upper_hsv2)
        mask = mask1 | mask2

        # Clean up the mask
        mask = cv2.medianBlur(mask, 5)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Find the largest contour assuming it’s the opponent
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > 500:  # threshold area to filter noise
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    # Draw the contour and center for visualization
                    cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
                    cv2.circle(frame, (cX, cY), 5, (255, 0, 0), -1)
                    return (cX, cY)
                else:
                    logging.warning("Contour moment calculation failed.")
        return None
