import core.config as config

def elbow_feedback(elbow_angle):
    low, high = config.IDEAL_ELBOW_ANGLE

    if elbow_angle < low:
        return "Raise your shooting elbow higher."

    if elbow_angle > high:
        return "Lower your shooting elbow slightly."

    return None


def knee_feedback(knee_angle):
    low, high = config.IDEAL_KNEE_ANGLE

    if knee_angle < low:
        return "Bend your knees more before you shoot."

    if knee_angle > high:
        return "Use less leg drive on the shot."

    return None


def velocity_feedback(release_velocity):
    if release_velocity < config.MIN_RELEASE_VELOCITY:
        return "Add more power to your release."

    return None


def generate(features):
    elbow_angle, knee_angle, _, release_velocity, *_ = features

    tips = [
        elbow_feedback(elbow_angle),
        knee_feedback(knee_angle),
        velocity_feedback(release_velocity)
    ]

    return [tip for tip in tips if tip]
