import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

from core.config import MODEL_PATH


def evaluate(csv_path):
    df = pd.read_csv(csv_path)

    X = df.drop(columns=["made"])
    y = df["made"]

    model = joblib.load(
        MODEL_PATH
    )

    predictions = model.predict(X)

    print()
    print("Accuracy :", accuracy_score(y, predictions))
    print("Precision :", precision_score(y, predictions))
    print("Recall :", recall_score(y, predictions))
    print("F1 :", f1_score(y, predictions))
    print()
    print(confusion_matrix(y, predictions))