# Camera

CAMERA_INDEX = 0
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
FPS = 30

# Drawing

FONT_SCALE = 0.8
FONT_THICKNESS = 2

GREEN = (0, 255, 0)
RED = (0, 0, 255)
BLUE = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (0, 255, 255)

# Pose
POSE_MODEL_PATH = "assets/models/pose_landmarker_lite.task"

# Ball Detection
YOLO_MODEL_PATH = "assets/models/basketball_yolo11n_v2.pt"
YOLO_CONFIDENCE = 0.4
BALL_CLASS_ID = 0  # fine-tuned single-class model. Was 32 (COCO "sports ball") for stock yolo11n.pt.

# Ball Detector Fine-Tuning
BALL_FRAMES_DIR = "dataset/ball_frames"
BALL_DATASET_YAML = "assets/dataset/data.yaml"
YOLO_EPOCHS = 50
YOLO_IMG_SIZE = 512


# Motion
VELOCITY_HISTORY = 5

# Shot Detection
RISE_WINDOW = 4
MAX_SHOT_FRAMES = 90
MAX_LOST_FRAMES = 10
RESULT_DISPLAY_FRAMES = 60

# Dataset
DATASET_PATH = "dataset/dataset.csv"

FEATURE_NAMES = [
    "elbow_angle",
    "knee_angle",
    "shoulder_angle",
    "release_velocity",
    "arc_height",
    "entry_angle",
    "wrist_ball_distance"
]

LABEL_NAME = "made"

# Model
MODEL_PATH = "models/model.pkl"

# Feedback
IDEAL_ELBOW_ANGLE = (80, 110)
IDEAL_KNEE_ANGLE = (100, 160)
MIN_RELEASE_VELOCITY = 0.02

# Display
WINDOW_NAME = "Basketball AI Shot Predictor"