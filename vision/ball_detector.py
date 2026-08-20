from ultralytics import YOLO

import core.config as config
from utils.drawing import circle

class BallDetector:
    def __init__(self):
        self.model = YOLO(config.YOLO_MODEL_PATH)
        self.position = None


    def process(self, frame):
        self.position = None

        results = self.model.predict(
            frame,
            classes=[config.BALL_CLASS_ID],
            conf=config.YOLO_CONFIDENCE,
            verbose=False
        )[0]

        if len(results.boxes):
            box = max(results.boxes, key=lambda b: float(b.conf))

            x1, y1, x2, y2 = box.xyxy[0].tolist()

            self.position = (int((x1 + x2) / 2), int((y1 + y2) / 2))
            radius = int(max(x2 - x1, y2 - y1) / 2)

            circle(frame, self.position, radius)

        return frame
