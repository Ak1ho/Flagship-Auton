# robot_detection.py
import cv2
import numpy as np

class RobotDetector:
    """
    Advanced classical CV approach combining:
      - Background Subtraction (motion detection)
      - (Optional) Color Filtering
      - Contour-based analysis
    No training required, but requires environment-based tuning.

    Usage:
      1. Create once with `RobotDetector(...)`.
      2. Call `detect_robot(frame)` each loop to get (cx, cy) or None.
    """

    def __init__(self,
                 min_area=500,
                 use_color_filter=False,
                 lower_color=(0, 0, 0),   # HSV lower bound
                 upper_color=(179, 255, 255), # HSV upper bound
                 history=500,
                 var_threshold=16):
        """
        :param min_area: Minimum contour area to consider a valid robot.
        :param use_color_filter: Whether to combine color-based filtering with motion detection.
        :param lower_color, upper_color: (H, S, V) ranges for color filtering.
        :param history: Number of frames for background subtractor to build a stable background model.
        :param var_threshold: Threshold for background subtractor's internal segmentation.
        """
        self.min_area = min_area
        self.use_color_filter = use_color_filter
        self.lower_color = lower_color
        self.upper_color = upper_color

        # Create a background subtractor. MOG2 is generally robust to some lighting changes.
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=history, varThreshold=var_threshold, detectShadows=True
        )

        # Morphology kernel to help clean up noise
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    def detect_robot(self, frame):
        """
        Returns (cx, cy) for the largest valid "robot" contour, or None if none found.
        Steps:
          1) Convert to HSV if color_filter is used
          2) Apply color mask if requested
          3) Apply background subtraction to isolate motion
          4) Morphological cleanup
          5) Find contours, pick largest above min_area
        """
        # 1) (Optional) color filtering in HSV space
        if self.use_color_filter:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            color_mask = cv2.inRange(hsv, self.lower_color, self.upper_color)
        else:
            # If no color filtering, just create a mask of all 255
            color_mask = np.ones(frame.shape[:2], dtype=np.uint8) * 255

        # 2) Background subtractor mask
        fg_mask = self.bg_subtractor.apply(frame)

        # The subtractor might label shadows differently. We can threshold them out:
        # Everything > 127 is considered foreground
        _, fg_mask = cv2.threshold(fg_mask, 127, 255, cv2.THRESH_BINARY)

        # Combine color_mask AND foreground mask
        combined_mask = cv2.bitwise_and(color_mask, fg_mask)

        # 3) Morphological operations to reduce noise
        # E.g., close small holes
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, self.kernel, iterations=2)
        # Erode + Dilate to remove small specks
        combined_mask = cv2.erode(combined_mask, self.kernel, iterations=1)
        combined_mask = cv2.dilate(combined_mask, self.kernel, iterations=2)

        # 4) Find contours in the mask
        contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        best_contour = None
        best_area = 0
        for c in contours:
            area = cv2.contourArea(c)
            if area >= self.min_area and area > best_area:
                best_area = area
                best_contour = c

        if best_contour is None:
            return None  # No valid robot found

        # 5) Compute bounding box & center
        x, y, w, h = cv2.boundingRect(best_contour)
        cx = x + w // 2
        cy = y + h // 2

        return (cx, cy)
