import csv
import os

import cv2

import core.config as config
from features.extract_features import extract
from utils.drawing import text
from utils.fps import FPSCounter
from utils.logger import Logger
from vision.ball_detector import BallDetector
from vision.camera import Camera
from vision.pose_detector import PoseDetector
from vision.tracker import Tracker


def write_row(path, row):
    exists = os.path.isfile(path)

    with open(path, "a", newline="") as file:
        writer = csv.writer(file)

        if not exists:
            writer.writerow(config.FEATURE_NAMES + [config.LABEL_NAME])

        writer.writerow(row)


def collect(csv_path):
    logger = Logger()

    camera = Camera(
        config.CAMERA_INDEX,
        config.FRAME_WIDTH,
        config.FRAME_HEIGHT
    )

    pose = PoseDetector()
    ball = BallDetector()
    tracker = Tracker()
    fps = FPSCounter()

    recording = False

    while True:
        success, frame = camera.read()

        if not success:
            logger.error(success)
            break

        frame = pose.process(frame)
        frame = ball.process(frame)

        landmarks = pose.get_landmarks(config.FRAME_WIDTH, config.FRAME_HEIGHT)

        if recording:
            tracker.update(ball.position)

        text(
            frame,
            "RECORDING" if recording else "READY",
            (20, 70),
            config.YELLOW if recording else config.WHITE
        )

        text(
            frame,
            "s: start | m: made | x: missed | q: quit",
            (20, config.FRAME_HEIGHT - 20),
            config.WHITE
        )

        fps.draw(frame)

        cv2.imshow(config.WINDOW_NAME, frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):
            tracker = Tracker()
            recording = True

            logger.info("Recording started")

        elif key in (ord("m"), ord("x")) and recording:
            features = extract(
                landmarks,
                tracker.trajectory(),
                config.FRAME_WIDTH,
                config.FRAME_HEIGHT
            )

            if features is None:
                logger.warning("Not enough data, sample discarded")
            else:
                label = 1 if key == ord("m") else 0

                write_row(csv_path, features + [label])

                logger.info(f"Sample saved (made={label})")

            recording = False

        elif key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    collect(config.DATASET_PATH)
