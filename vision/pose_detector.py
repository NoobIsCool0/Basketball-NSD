import time

import cv2
import mediapipe as mp

from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision

import core.config as config
from utils.drawing import circle

LANDMARK_NAMES = [
    "NOSE", "LEFT_EYE_INNER", "LEFT_EYE", "LEFT_EYE_OUTER",
    "RIGHT_EYE_INNER", "RIGHT_EYE", "RIGHT_EYE_OUTER",
    "LEFT_EAR", "RIGHT_EAR", "MOUTH_LEFT", "MOUTH_RIGHT",
    "LEFT_SHOULDER", "RIGHT_SHOULDER", "LEFT_ELBOW", "RIGHT_ELBOW",
    "LEFT_WRIST", "RIGHT_WRIST", "LEFT_PINKY", "RIGHT_PINKY",
    "LEFT_INDEX", "RIGHT_INDEX", "LEFT_THUMB", "RIGHT_THUMB",
    "LEFT_HIP", "RIGHT_HIP", "LEFT_KNEE", "RIGHT_KNEE",
    "LEFT_ANKLE", "RIGHT_ANKLE", "LEFT_HEEL", "RIGHT_HEEL",
    "LEFT_FOOT_INDEX", "RIGHT_FOOT_INDEX"
]

class PoseDetector:
    def __init__(self):
        options = mp_vision.PoseLandmarkerOptions(
            base_options=mp_python.BaseOptions(
                model_asset_path=config.POSE_MODEL_PATH
            ),
            running_mode=mp_vision.RunningMode.VIDEO
        )

        self.landmarker = mp_vision.PoseLandmarker.create_from_options(options)
        self.start_time = time.time()

        self.landmarks = None


    def process(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        timestamp_ms = int((time.time() - self.start_time) * 1000)

        result = self.landmarker.detect_for_video(image, timestamp_ms)

        self.landmarks = result.pose_landmarks[0] if result.pose_landmarks else None

        if self.landmarks:
            height, width = frame.shape[:2]

            for landmark in self.landmarks:
                circle(
                    frame,
                    (int(landmark.x * width), int(landmark.y * height)),
                    3
                )

        return frame


    def get_landmarks(self, frame_width, frame_height):
        if not self.landmarks:
            return None

        return {
            name: (
                self.landmarks[i].x * frame_width,
                self.landmarks[i].y * frame_height
            )
            for i, name in enumerate(LANDMARK_NAMES)
        }
