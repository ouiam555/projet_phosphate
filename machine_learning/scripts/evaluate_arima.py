import math

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error,
)

from load_data import load_data


def main() -> None:
    df = load_data()

    time_series = df[
        ["YEAR", "MONTH_NUMBER", "PHOSPHATE_PRICE_USD"]
    ].copy()

    time_series["DATE"] = pd.to_datetime(
        dict(
            year=time_series["YEAR"],
            month=time_series["MONTH_NUMBER"],
            day=1,
        )
    )

    time_series = (
        time_series
        .sort_values("DATE")
        .set_index("DATE")
    )

    series = time_series["PHOSPHATE_PRICE_USD"].astype(float)

    train = series.iloc[:-12].copy()
    test = series.iloc[-12:].copy()

    # ARIMA(p, d, q)
    model = ARIMA(
        train,
        order=(2, 1, 2),
    )

    fitted_model = model.fit()

    predictions = fitted_model.forecast(
        steps=len(test)
    )

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

    print("\n===== ARIMA EVALUATION =====")
    print(f"Training rows : {len(train)}")
    print(f"Testing rows  : {len(test)}")

    print(f"\nMAE  : {mae:.2f}")
    print(f"RMSE : {rmse:.2f}")
    print(f"MAPE : {mape:.2f}%")

    results = pd.DataFrame({
        "DATE": test.index,
        "REAL": test.values,
        "PREDICTED": predictions.values,
    })

    results["ABSOLUTE_ERROR"] = abs(
        results["REAL"] - results["PREDICTED"]
    )

    print("\n===== REAL VS PREDICTED =====")
    print(results.to_string(index=False))

    results.to_csv(
        "reports/arima_evaluation.csv",
        index=False,
    )

    print("\nResults saved to: reports/arima_evaluation.csv")


if __name__ == "__main__":
    main()