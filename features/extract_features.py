import math

from features.angles import angle
from features.normalize import scale
from features.trajectory import arc_height, entry_angle
from features.velocity import average_speed
from utils.helpers import distance


def extract(landmarks, ball_trajectory, frame_width, frame_height):
    if not landmarks or len(ball_trajectory) < 2:
        return None

    reference = math.hypot(frame_width, frame_height)

    elbow_angle = angle(
        landmarks["RIGHT_SHOULDER"],
        landmarks["RIGHT_ELBOW"],
        landmarks["RIGHT_WRIST"]
    )

    knee_angle = angle(
        landmarks["RIGHT_HIP"],
        landmarks["RIGHT_KNEE"],
        landmarks["RIGHT_ANKLE"]
    )

    shoulder_angle = angle(
        landmarks["RIGHT_ELBOW"],
        landmarks["RIGHT_SHOULDER"],
        landmarks["RIGHT_HIP"]
    )

    release_velocity = scale(average_speed(ball_trajectory), reference)
    height = scale(arc_height(ball_trajectory), reference)
    entry = entry_angle(ball_trajectory)

    wrist_ball_distance = scale(
        distance(landmarks["RIGHT_WRIST"], ball_trajectory[-1]),
        reference
    )

    return [
        elbow_angle,
        knee_angle,
        shoulder_angle,
        release_velocity,
        height,
        entry,
        wrist_ball_distance
    ]
