# Basketball AI Shot Predictor

Webcam-based basketball shot analysis. Tracks pose and ball motion, extracts
shooting-form features, and predicts make/miss with coaching feedback from a
trained classifier.

## Structure

```
core/config.py          All configurable values
main.py                 Entry point (live camera + pose/ball overlay)

vision/                 Camera capture, pose estimation, ball detection, tracking
features/               Turns landmarks + ball trajectory into a feature vector
feedback/               Scoring, coaching tips, on-screen overlay
models/                 Training, evaluation, and inference (RandomForest)
dataset/                Data collection and preprocessing
utils/                  Drawing, FPS counter, logging, math helpers
```

## Setup

```bash
pip install -r requirements.txt
```

Two model files are needed and are not committed to the repo:

- **Pose Landmarker** (`assets/models/pose_landmarker_lite.task`) — mediapipe's
  Tasks API needs this downloaded manually, it isn't bundled with the
  package:

  ```bash
  curl -L -o assets/models/pose_landmarker_lite.task "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/latest/pose_landmarker_lite.task"
  ```

- **YOLO11n** (`assets/models/yolo11n.pt`) — downloads automatically the
  first time `BallDetector` runs (via Ultralytics), no action needed.

## Usage

1. **Collect training samples** — run this while shooting in front of the
   camera. Press `s` to start tracking a shot attempt, `m` once it goes in,
   `x` once it misses, `q` to quit. Each labeled attempt is appended to
   `dataset/dataset.csv`.

   ```bash
   python -m dataset.collect_data
   ```

2. **Preprocess** the collected data (drops empty/duplicate rows in place):

   ```bash
   python -m dataset.preprocess
   ```

3. **Train** the model (writes `models/model.pkl`):

   ```bash
   python -m models.train_model
   ```

4. **Evaluate** accuracy/precision/recall/F1 on the same dataset:

   ```bash
   python -m models.evaluate
   ```

5. **Run** the live camera app. It auto-detects a shot attempt (ball rising
   near the player), tracks it until it lands, then predicts make/miss and
   shows coaching tips on screen:

   ```bash
   python main.py
   ```

## Fine-tuning the ball detector

The default `yolo11n.pt` only knows COCO's generic "sports ball" class, so
it won't be tuned to your specific ball/camera/lighting. To fine-tune it:

1. **Collect raw frames** from your actual setup — run this and press
   `space` to save the current frame (no overlay burned in) whenever the
   ball is visible, in different positions/lighting/angles. Frames go to
   `dataset/ball_frames/`.

   ```bash
   python -m dataset.collect_ball_frames
   ```

2. **Label the frames** — draw a bounding box around the ball in each
   image. This has to be done outside this repo, e.g. with
   [Roboflow](https://roboflow.com) (free tier, browser-based) or
   [LabelImg](https://github.com/HumanSignal/labelImg) (local). Export in
   YOLO format to `dataset/ball_yolo/` — this should give you a
   `data.yaml` plus `images/`/`labels/` train/val folders (matching
   `config.BALL_DATASET_YAML`). A single class ("basketball", id `0`) is
   enough. For best results, mix in a public basketball dataset from
   Roboflow Universe alongside your own frames rather than starting from
   only a few hundred self-labeled images.

3. **Fine-tune** — starts from whatever `config.YOLO_MODEL_PATH` currently
   points to (the stock `yolo11n.pt` by default) and trains on your
   labeled set. Results (including the new weights) land in
   `runs/detect/trainX/weights/best.pt`.

   ```bash
   python -m models.train_yolo
   ```

4. **Switch to the fine-tuned weights** — copy `best.pt` into
   `assets/models/`, then in `core/config.py` point `YOLO_MODEL_PATH` at
   it and set `BALL_CLASS_ID = 0` (your new single-class model's only
   class, instead of COCO's class `32`).

## Configuration

All tunables live in `core/config.py`. Camera index, `YOLO_CONFIDENCE`, and
the ideal-form feedback ranges are placeholder defaults — they need to be
checked against your own camera and shooting form before results are
meaningful.

## Status

`main.py` now runs the full pipeline end to end: camera -> pose (mediapipe
Tasks API `PoseLandmarker`) -> ball detection (YOLO11n) -> automatic
shot-attempt tracking -> feature extraction -> prediction -> coaching
feedback overlay. If `models/model.pkl` doesn't exist yet, it starts in
detection-only mode (no predictions) instead of crashing.

What's still on you before it's actually useful:

- No dataset has been collected and no model has been trained yet — run
  steps 1-3 above with real shooting data first.
- Ball detection uses YOLO11n's stock COCO-pretrained weights and its
  generic "sports ball" class — it isn't basketball-specific, so it'll also
  fire on a soccer ball, tennis ball, etc. If that's ever a problem, the fix
  is fine-tuning on a basketball-specific dataset, not a config change.
- The shot-detection timing constants (`RISE_WINDOW`, `MAX_SHOT_FRAMES`,
  `MAX_LOST_FRAMES`, `RESULT_DISPLAY_FRAMES` in `core/config.py`) are
  generic defaults tuned for nothing in particular — check them against
  your own camera and frame rate.
- Shot-attempt detection is a simple heuristic (ball rising near the player
  starts tracking; landing, timing out, or losing the ball ends it) — it
  will misfire on passes, rebounds, or anything else that looks like an
  upward ball motion.
