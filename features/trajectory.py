import math


def arc_height(positions):
    if not positions:
        return 0

    release_y = positions[0][1]
    apex_y = min(p[1] for p in positions)

    return release_y - apex_y


def entry_angle(positions):
    if len(positions) < 2:
        return 0

    (x1, y1), (x2, y2) = positions[-2], positions[-1]

    return math.degrees(math.atan2(y2 - y1, x2 - x1))


def apex(positions):
    if not positions:
        return None

    return min(positions, key=lambda p: p[1])
