import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from load_data import load_data
from feature_engineering import create_features


def train_baseline():
    df = load_data()
    df = create_features(df)

    train_df = df.iloc[:-12].copy()
    test_df = df.iloc[-12:].copy()

    y_true = test_df["PHOSPHATE_PRICE_USD"]
    y_pred = test_df["PRICE_LAG_1"]

    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)

    print("\nBaseline model completed successfully.")
    print(f"Training rows: {len(train_df)}")
    print(f"Testing rows: {len(test_df)}")

    print("\n========== BASELINE METRICS ==========")
    print(f"MAE:  {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R²:   {r2:.4f}")

    results = test_df[
        ["DATE", "PHOSPHATE_PRICE_USD", "PRICE_LAG_1"]
    ].copy()

    results = results.rename(
        columns={
            "PHOSPHATE_PRICE_USD": "ACTUAL_PRICE",
            "PRICE_LAG_1": "PREDICTED_PRICE",
        }
    )

    print("\n========== PREDICTIONS ==========")
    print(results.to_string(index=False))


if __name__ == "__main__":
    train_baseline()