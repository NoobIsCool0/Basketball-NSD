import cv2
import time

import core.config as config

class FPSCounter:
    def __init__(self):
        self.previous = time.time()
        self.fps = 0


    def update(self):
        current = time.time()

        delta = current - self.previous

        self.previous = current

        if delta > 0:
            self.fps = 1 / delta


    def draw(self, frame):
        self.update()

        cv2.putText(
            frame,
            f"FPS : {int(self.fps)}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            config.FONT_SCALE,
            config.GREEN,
            config.FONT_THICKNESS
        )