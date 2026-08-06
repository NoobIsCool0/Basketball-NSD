from dataclasses import dataclass

@dataclass
class PredictionResult:

    prediction: bool
    confidence: float
    probability: list[float]