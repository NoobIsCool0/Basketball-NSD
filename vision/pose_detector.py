import cv2
import mediapipe as mp


class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils

        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.landmarks = None


    def process(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.pose.process(rgb)

        self.landmarks = results.pose_landmarks

        if self.landmarks:
            self.mp_drawing.draw_landmarks(
                frame,
                self.landmarks,
                self.mp_pose.POSE_CONNECTIONS
            )

        return frame


    def get_landmarks(self, frame_width, frame_height):
        if not self.landmarks:
            return None

        return {
            landmark.name: (
                self.landmarks.landmark[landmark.value].x * frame_width,
                self.landmarks.landmark[landmark.value].y * frame_height
            )
            for landmark in self.mp_pose.PoseLandmark
        }
