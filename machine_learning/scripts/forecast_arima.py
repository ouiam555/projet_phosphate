from pathlib import Path

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

from load_data import load_data


FORECAST_END_YEAR = 2030


def main() -> None:
    df = load_data()

    ts = df[
        [
            "YEAR",
            "MONTH_NUMBER",
            "PHOSPHATE_PRICE_USD",
        ]
    ].copy()

    ts["DATE"] = pd.to_datetime(
        dict(
            year=ts["YEAR"],
            month=ts["MONTH_NUMBER"],
            day=1,
        )
    )

    ts = (
        ts
        .sort_values("DATE")
        .set_index("DATE")
        .asfreq("MS")
    )

    series = (
        ts["PHOSPHATE_PRICE_USD"]
        .astype(float)
        .interpolate(method="time")
    )

    model = ARIMA(
        series,
        order=(2, 1, 2),
    )

    fitted_model = model.fit()

    last_date = series.index.max()

    forecast_end = pd.Timestamp(
        year=FORECAST_END_YEAR,
        month=12,
        day=1,
    )

    forecast_months = (
        (forecast_end.year - last_date.year) * 12
        + (forecast_end.month - last_date.month)
    )

    forecast_result = fitted_model.get_forecast(
        steps=forecast_months
    )

    predicted_mean = forecast_result.predicted_mean

    confidence_interval = (
        forecast_result.conf_int(alpha=0.05)
    )

    future_dates = pd.date_range(
        start=last_date + pd.offsets.MonthBegin(1),
        periods=forecast_months,
        freq="MS",
    )

    forecast_df = pd.DataFrame(
        {
            "DATE": future_dates,
            "YEAR": future_dates.year,
            "MONTH_NUMBER": future_dates.month,
            "FORECAST_PRICE_USD": predicted_mean.values,
            "LOWER_95": confidence_interval.iloc[:, 0].values,
            "UPPER_95": confidence_interval.iloc[:, 1].values,
        }
    )

    numeric_columns = [
        "FORECAST_PRICE_USD",
        "LOWER_95",
        "UPPER_95",
    ]

    forecast_df[numeric_columns] = (
        forecast_df[numeric_columns]
        .round(2)
    )

    reports_folder = Path("reports")
    reports_folder.mkdir(exist_ok=True)

    output_path = (
        reports_folder
        / "forecast_price_2030.csv"
    )

    forecast_df.to_csv(
        output_path,
        index=False,
    )

    print("\n===== ARIMA FORECAST WITH 95% CI =====")

    print("\nFirst forecasts:")
    print(forecast_df.head().to_string(index=False))

    print("\nLast forecasts:")
    print(forecast_df.tail().to_string(index=False))

    print("\nForecast period:")
    print(
        f"{forecast_df['DATE'].min().date()} "
        f"to {forecast_df['DATE'].max().date()}"
    )

    print(
        f"\nRows generated: {len(forecast_df)}"
    )

    print(
        f"Saved to: {output_path}"
    )


if __name__ == "__main__":
    main()