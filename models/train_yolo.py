from ultralytics import YOLO

import core.config as config

def train(data_yaml):
    model = YOLO(config.YOLO_MODEL_PATH)

    model.train(
        data=data_yaml,
        epochs=config.YOLO_EPOCHS,
        imgsz=config.YOLO_IMG_SIZE
    )


if __name__ == "__main__":
    train(config.BALL_DATASET_YAML)
