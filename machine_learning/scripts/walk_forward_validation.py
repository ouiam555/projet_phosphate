from pathlib import Path
import math

import pandas as pd

from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error,
)

from load_data import load_data


TEST_YEARS = [2020, 2021, 2022, 2023, 2024, 2025]


def prepare_series() -> pd.Series:
    df = load_data()

    ts = df[
        ["YEAR", "MONTH_NUMBER", "PHOSPHATE_PRICE_USD"]
    ].copy()

    ts["DATE"] = pd.to_datetime(
        dict(
            year=ts["YEAR"],
            month=ts["MONTH_NUMBER"],
            day=1,
        )
    )

    ts = (
        ts.sort_values("DATE")
        .set_index("DATE")
        .asfreq("MS")
    )

    # November 2023 is missing, so interpolate it
    series = (
        ts["PHOSPHATE_PRICE_USD"]
        .astype(float)
        .interpolate(method="time")
    )

    return series


def evaluate_year(
    series: pd.Series,
    test_year: int,
) -> dict | None:

    train_end = pd.Timestamp(
        year=test_year - 1,
        month=12,
        day=1,
    )

    test_start = pd.Timestamp(
        year=test_year,
        month=1,
        day=1,
    )

    test_end = pd.Timestamp(
        year=test_year,
        month=12,
        day=1,
    )

    train = series.loc[:train_end].copy()
    test = series.loc[test_start:test_end].copy()

    if len(train) < 24:
        print(
            f"Skipping {test_year}: "
            "not enough training observations."
        )
        return None

    if len(test) == 0:
        print(
            f"Skipping {test_year}: "
            "no test observations."
        )
        return None

    model = ARIMA(
        train,
        order=(2, 1, 2),
    )

    fitted_model = model.fit()

    predictions = fitted_model.forecast(
        steps=len(test)
    )

    predictions.index = test.index

    mae = mean_absolute_error(
        test,
        predictions,
    )

    mse = mean_squared_error(
        test,
        predictions,
    )

    rmse = math.sqrt(mse)

    mape = (
        mean_absolute_percentage_error(
            test,
            predictions,
        )
        * 100
    )

    return {
        "TEST_YEAR": test_year,
        "TRAINING_ROWS": len(train),
        "TESTING_ROWS": len(test),
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape,
        "REAL_MEAN": test.mean(),
        "PREDICTED_MEAN": predictions.mean(),
    }


def main() -> None:
    series = prepare_series()

    results = []

    for year in TEST_YEARS:
        print(f"\nEvaluating year {year}...")

        result = evaluate_year(
            series=series,
            test_year=year,
        )

        if result is not None:
            results.append(result)

    results_df = pd.DataFrame(results)

    if results_df.empty:
        raise ValueError(
            "No evaluation results were generated."
        )

    results_df = results_df.sort_values(
        "TEST_YEAR"
    ).reset_index(drop=True)

    print("\n===== ARIMA WALK-FORWARD VALIDATION =====")

    print(
        results_df.to_string(
            index=False,
            formatters={
                "MAE": "{:.2f}".format,
                "RMSE": "{:.2f}".format,
                "MAPE": "{:.2f}%".format,
                "REAL_MEAN": "{:.2f}".format,
                "PREDICTED_MEAN": "{:.2f}".format,
            },
        )
    )

    print("\n===== GLOBAL METRICS =====")

    print(
        f"Average MAE  : "
        f"{results_df['MAE'].mean():.2f}"
    )

    print(
        f"Average RMSE : "
        f"{results_df['RMSE'].mean():.2f}"
    )

    print(
        f"Average MAPE : "
        f"{results_df['MAPE'].mean():.2f}%"
    )

    reports_folder = Path("reports")
    reports_folder.mkdir(exist_ok=True)

    output_path = (
        reports_folder
        / "arima_walk_forward_validation.csv"
    )

    results_df.to_csv(
        output_path,
        index=False,
    )

    print(
        f"\nResults saved to: {output_path}"
    )


if __name__ == "__main__":
    main()