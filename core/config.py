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

# Ball Detection
BALL_MIN_RADIUS = 8
BALL_MAX_RADIUS = 80

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