def scale(value, reference):
    if reference == 0:
        return 0

    return value / reference


def normalize_point(point, width, height):
    return (point[0] / width, point[1] / height)


def normalize_landmarks(landmarks, width, height):
    return {
        name: normalize_point(point, width, height)
        for name, point in landmarks.items()
    }
