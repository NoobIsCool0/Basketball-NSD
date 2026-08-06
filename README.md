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

## Configuration

All tunables live in `core/config.py`. Camera index, ball detector color/size
thresholds, and the ideal-form feedback ranges are placeholder defaults —
they need to be calibrated against your own camera, lighting, and ball
before results are meaningful.

## Status

`main.py` now runs the full pipeline end to end: camera -> pose/ball
detection -> automatic shot-attempt tracking -> feature extraction ->
prediction -> coaching feedback overlay. If `models/model.pkl` doesn't
exist yet, it starts in detection-only mode (no predictions) instead of
crashing.

What's still on you before it's actually useful:

- No dataset has been collected and no model has been trained yet — run
  steps 1-3 above with real shooting data first.
- Ball-color thresholds in `vision/ball_detector.py`, the ball size range,
  and the shot-detection timing constants (`RISE_WINDOW`, `MAX_SHOT_FRAMES`,
  `MAX_LOST_FRAMES`, `RESULT_DISPLAY_FRAMES` in `core/config.py`) are all
  generic defaults tuned for nothing in particular — they need to be
  checked against your own camera, ball, and frame rate.
- Shot-attempt detection is a simple heuristic (ball rising near the player
  starts tracking; landing, timing out, or losing the ball ends it) — it
  will misfire on passes, rebounds, or anything else that looks like an
  upward ball motion.
