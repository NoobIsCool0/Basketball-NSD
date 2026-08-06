import pandas as pd

import core.config as config

def preprocess(csv_path):
    df = pd.read_csv(csv_path)

    before = len(df)

    df = df.dropna()
    df = df.drop_duplicates()

    df.to_csv(csv_path, index=False)

    print(f"Rows : {before} -> {len(df)}")


if __name__ == "__main__":
    preprocess(config.DATASET_PATH)
