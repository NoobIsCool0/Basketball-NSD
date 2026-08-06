import cv2

import core.config as config

def text(frame, string, position, color=config.WHITE):
    cv2.putText(
        frame,
        string,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        config.FONT_SCALE,
        color,
        config.FONT_THICKNESS
    )


def circle(frame, center, radius, color=config.GREEN):
    cv2.circle(
        frame,
        center,
        radius,
        color,
        2
    )


def line(frame, p1, p2, color=config.BLUE):
    cv2.line(
        frame,
        p1,
        p2,
        color,
        2
    )