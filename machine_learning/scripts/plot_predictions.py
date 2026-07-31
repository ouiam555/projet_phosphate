from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd

from load_data import load_data
from feature_engineering import create_features


def main() -> None:
    df = load_data()
    df = create_features(df)

    test = df.iloc[-12:].copy()

    model = joblib.load(
        "models/random_forest_price_model.joblib"
    )

    feature_columns = joblib.load(
        "models/feature_columns.joblib"
    )

    X_test = test[feature_columns]

    predictions = model.predict(X_test)

    results = pd.DataFrame({
        "DATE": test["DATE"],
        "ACTUAL_PRICE": test["PHOSPHATE_PRICE_USD"],
        "PREDICTED_PRICE": predictions,
    })

    reports_folder = Path("reports")
    reports_folder.mkdir(exist_ok=True)

    csv_path = reports_folder / "random_forest_predictions.csv"
    image_path = reports_folder / "actual_vs_predicted.png"

    results.to_csv(csv_path, index=False)

    plt.figure(figsize=(11, 6))

    plt.plot(
        results["DATE"],
        results["ACTUAL_PRICE"],
        marker="o",
        label="Actual Price",
    )

    plt.plot(
        results["DATE"],
        results["PREDICTED_PRICE"],
        marker="o",
        label="Predicted Price",
    )

    plt.title("Actual vs Predicted Phosphate Prices")
    plt.xlabel("Date")
    plt.ylabel("Price USD per Metric Ton")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        image_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.show()

    print("\n===== PREDICTIONS EXPORTED =====")
    print(f"CSV saved to: {csv_path}")
    print(f"Chart saved to: {image_path}")


if __name__ == "__main__":
    main()