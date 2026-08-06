import math

def distance(p1, p2):
    return math.sqrt(
        (p2[0] - p1[0]) ** 2 +
        (p2[1] - p1[1]) ** 2
    )

def midpoint(p1, p2):
    return (
        (p1[0] + p2[0]) / 2,
        (p1[1] + p2[1]) / 2
    )

def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))