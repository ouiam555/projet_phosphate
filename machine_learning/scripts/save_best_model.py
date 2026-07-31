from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestRegressor

from load_data import load_data
from feature_engineering import create_features


def main() -> None:
    df = load_data()
    df = create_features(df)

    feature_columns = [
        column
        for column in df.columns
        if column not in ["DATE", "PHOSPHATE_PRICE_USD"]
    ]

    X = df[feature_columns]
    y = df["PHOSPHATE_PRICE_USD"]

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=8,
        min_samples_split=4,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X, y)

    models_folder = Path("models")
    models_folder.mkdir(exist_ok=True)

    model_path = models_folder / "random_forest_price_model.joblib"
    features_path = models_folder / "feature_columns.joblib"

    joblib.dump(model, model_path)
    joblib.dump(feature_columns, features_path)

    print("\n===== BEST MODEL SAVED =====")
    print(f"Model: Random Forest")
    print(f"Training rows: {len(df)}")
    print(f"Model saved to: {model_path}")
    print(f"Features saved to: {features_path}")


if __name__ == "__main__":
    main()