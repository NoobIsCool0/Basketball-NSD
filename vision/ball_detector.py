import cv2
import numpy as np

import core.config as config
from utils.drawing import circle


class BallDetector:
    LOWER_ORANGE = np.array([5, 100, 100])
    UPPER_ORANGE = np.array([20, 255, 255])

    def __init__(self):
        self.position = None


    def process(self, frame):
        self.position = None

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.LOWER_ORANGE, self.UPPER_ORANGE)

        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if contours:
            largest = max(contours, key=cv2.contourArea)

            (x, y), radius = cv2.minEnclosingCircle(largest)

            if config.BALL_MIN_RADIUS <= radius <= config.BALL_MAX_RADIUS:
                self.position = (int(x), int(y))

                circle(frame, self.position, int(radius))

        return frame
