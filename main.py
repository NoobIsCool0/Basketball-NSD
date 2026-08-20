import cv2

import core.config as config  # noqa: PLR0402
from features.extract_features import extract
from feedback.feedback import generate
from feedback.overlay import draw_prediction, draw_tips
from models.predictor import Predictor
from utils.fps import FPSCounter
from utils.logger import Logger
from vision.ball_detector import BallDetector
from vision.camera import Camera
from vision.pose_detector import PoseDetector
from vision.tracker import Tracker


def is_rising(positions):
    if len(positions) < 3:
        return False

    return all(
        positions[i][1] > positions[i + 1][1]
        for i in range(len(positions) - 1)
    )


def has_landed(positions):
    if len(positions) < 2:
        return False

    return positions[-1][1] >= positions[0][1]


def main():
    logger = Logger()

    camera = Camera(
        config.CAMERA_INDEX,
        config.FRAME_WIDTH,
        config.FRAME_HEIGHT
    )

    pose = PoseDetector()
    ball = BallDetector()
    fps = FPSCounter()

    try:
        predictor = Predictor()
    except FileNotFoundError:
        predictor = None
        logger.warning("No trained model found, running in detection-only mode")

    idle_window = Tracker(maxlen=config.RISE_WINDOW)
    shot = Tracker()

    tracking = False
    lost_frames = 0

    result = None
    tips = []
    result_timer = 0

    while True:
        success, frame = camera.read()

        if not success:
            logger.error(success)
            break

        frame = pose.process(frame)
        frame = ball.process(frame)

        landmarks = pose.get_landmarks(config.FRAME_WIDTH, config.FRAME_HEIGHT)

        if not tracking:
            if ball.position:
                idle_window.update(ball.position)

                if is_rising(idle_window.trajectory()):
                    tracking = True

                    shot = Tracker()

                    for position in idle_window.trajectory():
                        shot.update(position)
            else:
                idle_window = Tracker(maxlen=config.RISE_WINDOW)

        else:
            if ball.position:
                shot.update(ball.position)
                lost_frames = 0
            else:
                lost_frames += 1

            positions = shot.trajectory()

            done = (
                len(positions) >= config.MAX_SHOT_FRAMES
                or lost_frames >= config.MAX_LOST_FRAMES
                or has_landed(positions)
            )

            if done:
                features = extract(
                    landmarks,
                    positions,
                    config.FRAME_WIDTH,
                    config.FRAME_HEIGHT
                )

                if features and predictor:
                    result = predictor.predict(features)
                    tips = generate(features)
                    result_timer = config.RESULT_DISPLAY_FRAMES

                    logger.info(
                        f"Prediction : {'MADE' if result.prediction else 'MISSED'} "
                        f"({result.confidence * 100:.0f}%)"
                    )

                tracking = False
                lost_frames = 0
                idle_window = Tracker(maxlen=config.RISE_WINDOW)

        if result_timer > 0:
            draw_prediction(frame, result)
            draw_tips(frame, tips)

            result_timer -= 1

        fps.draw(frame)

        cv2.imshow(config.WINDOW_NAME, frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
