from pathlib import Path

import numpy as np
import pandas as pd

from load_data import load_data
from feature_engineering import create_features

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

from xgboost import XGBRegressor


def calculate_metrics(y_true, predictions) -> dict:
    return {
        "MAE": mean_absolute_error(y_true, predictions),
        "RMSE": np.sqrt(mean_squared_error(y_true, predictions)),
        "R2": r2_score(y_true, predictions),
    }


def main() -> None:
    df = load_data()
    df = create_features(df)

    train = df.iloc[:-12].copy()
    test = df.iloc[-12:].copy()

    excluded_columns = [
        "DATE",
        "PHOSPHATE_PRICE_USD",
    ]

    feature_columns = [
        column
        for column in df.columns
        if column not in excluded_columns
    ]

    X_train = train[feature_columns]
    y_train = train["PHOSPHATE_PRICE_USD"]

    X_test = test[feature_columns]
    y_test = test["PHOSPHATE_PRICE_USD"]

    results = []

    # Baseline
    baseline_predictions = test["PRICE_LAG_1"].to_numpy()

    results.append({
        "Model": "Baseline",
        **calculate_metrics(y_test, baseline_predictions),
    })

    # Linear Regression
    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)

    linear_predictions = linear_model.predict(X_test)

    results.append({
        "Model": "Linear Regression",
        **calculate_metrics(y_test, linear_predictions),
    })

    # Random Forest
    random_forest_model = RandomForestRegressor(
        n_estimators=300,
        max_depth=8,
        min_samples_split=4,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )

    random_forest_model.fit(X_train, y_train)

    random_forest_predictions = random_forest_model.predict(X_test)

    results.append({
        "Model": "Random Forest",
        **calculate_metrics(y_test, random_forest_predictions),
    })

    # XGBoost
    xgboost_model = XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
    )

    xgboost_model.fit(X_train, y_train)

    xgboost_predictions = xgboost_model.predict(X_test)

    results.append({
        "Model": "XGBoost",
        **calculate_metrics(y_test, xgboost_predictions),
    })

    comparison = pd.DataFrame(results)

    comparison = comparison.sort_values(
        by=["MAE", "RMSE"],
        ascending=True,
    ).reset_index(drop=True)

    print("\n===== MODEL COMPARISON =====")

    print(
        comparison.to_string(
            index=False,
            formatters={
                "MAE": "{:.2f}".format,
                "RMSE": "{:.2f}".format,
                "R2": "{:.4f}".format,
            },
        )
    )

    print("\nImportant note:")
    print(
        "The test target is constant at 152.5, "
        "so R² is not informative for this evaluation."
    )

    reports_folder = Path("reports")
    reports_folder.mkdir(exist_ok=True)

    output_path = reports_folder / "model_comparison.csv"

    comparison.to_csv(
        output_path,
        index=False,
    )

    print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()