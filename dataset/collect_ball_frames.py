import os

import cv2

import core.config as config

from vision.camera import Camera

from utils.drawing import text
from utils.logger import Logger

def next_index(directory):
    saved = [f for f in os.listdir(directory) if f.endswith(".jpg")]

    return len(saved)


def collect(output_dir):
    logger = Logger()

    os.makedirs(output_dir, exist_ok=True)

    camera = Camera(
        config.CAMERA_INDEX,
        config.FRAME_WIDTH,
        config.FRAME_HEIGHT
    )

    index = next_index(output_dir)

    while True:
        success, frame = camera.read()

        if not success:
            logger.error(success)
            break

        display = frame.copy()

        text(
            display,
            f"Saved : {index} | space: save frame | q: quit",
            (20, 40)
        )

        cv2.imshow(config.WINDOW_NAME, display)

        key = cv2.waitKey(1) & 0xFF

        if key == ord(" "):
            path = os.path.join(output_dir, f"frame_{index:05d}.jpg")

            cv2.imwrite(path, frame)

            index += 1

            logger.info(f"Saved {path}")

        elif key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    collect(config.BALL_FRAMES_DIR)
