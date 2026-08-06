import core.config as config
from utils.drawing import text

def draw_prediction(frame, prediction_result):
    label = "MADE" if prediction_result.prediction else "MISSED"
    color = config.GREEN if prediction_result.prediction else config.RED

    text(
        frame,
        f"{label} ({prediction_result.confidence * 100:.0f}%)",
        (20, 70),
        color
    )


def draw_tips(frame, tips):
    for i, tip in enumerate(tips):
        text(
            frame,
            tip,
            (20, 110 + i * 30),
            config.YELLOW
        )
