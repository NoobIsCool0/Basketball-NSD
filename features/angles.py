import math

def angle(a, b, c):
    ang1 = math.atan2(a[1] - b[1], a[0] - b[0])
    ang2 = math.atan2(c[1] - b[1], c[0] - b[0])

    result = abs(math.degrees(ang2 - ang1))

    if result > 180:
        result = 360 - result

    return result
