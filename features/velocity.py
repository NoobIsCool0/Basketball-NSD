from utils.helpers import distance


def average_speed(positions):
    if len(positions) < 2:
        return 0

    total = 0

    for i in range(1, len(positions)):
        total += distance(positions[i - 1], positions[i])

    return total / (len(positions) - 1)


def speed(p1, p2, dt):
    if dt <= 0:
        return 0

    return distance(p1, p2) / dt
