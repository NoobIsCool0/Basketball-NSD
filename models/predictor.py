import joblib
import numpy as np

from core.config import MODEL_PATH
from models.prediction_result import PredictionResult


class Predictor:
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)


    def predict(self, features) -> PredictionResult:
        probabilities = self.model.predict_proba([features])[0]

        prediction = bool(np.argmax(probabilities))
        confidence = float(np.max(probabilities))

        return PredictionResult(
            prediction=prediction,
            confidence=confidence,
            probability=probabilities.tolist()
        )