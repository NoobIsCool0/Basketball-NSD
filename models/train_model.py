import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score

from core.config import MODEL_PATH

def train(csv_path):
    df = pd.read_csv(csv_path)

    X = df.drop(columns=["made"])
    y = df["made"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print(f"Accuracy : {accuracy * 100:.2f}%")

    joblib.dump(
        model,
        MODEL_PATH
    )

    print("Model Saved")


if __name__ == "__main__":
    train("dataset/dataset.csv")