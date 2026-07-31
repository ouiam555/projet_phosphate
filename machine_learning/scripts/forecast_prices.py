from pathlib import Path

import joblib
import pandas as pd

from load_data import load_data
from feature_engineering import create_features


FORECAST_END_YEAR = 2030

ECONOMIC_COLUMNS = [
    "TOTAL_PRODUCTION_KTONS",
    "TOTAL_RESERVES_KTONS",
    "TOTAL_EXPORT_WEIGHT_KG",
    "TOTAL_EXPORT_VALUE_USD",
    "TOTAL_IMPORT_WEIGHT_KG",
    "TOTAL_IMPORT_VALUE_USD",
    "AVG_INFLATION_RATE",
]


def main() -> None:
    df_raw = load_data()
    df_features = create_features(df_raw)

    model = joblib.load(
        "models/random_forest_price_model.joblib"
    )

    feature_columns = joblib.load(
        "models/feature_columns.joblib"
    )

    # Historical prices after feature engineering.
    price_history = (
        df_features["PHOSPHATE_PRICE_USD"]
        .astype(float)
        .tolist()
    )

    # Last known economic values will be reused for future months.
    last_known_row = df_features.iloc[-1].copy()

    last_date = pd.Timestamp(
        year=int(last_known_row["YEAR"]),
        month=int(last_known_row["MONTH_NUMBER"]),
        day=1,
    )

    forecast_end_date = pd.Timestamp(
        year=FORECAST_END_YEAR,
        month=12,
        day=1,
    )

    future_dates = pd.date_range(
        start=last_date + pd.offsets.MonthBegin(1),
        end=forecast_end_date,
        freq="MS",
    )

    next_time_index = int(last_known_row["TIME_INDEX"]) + 1

    forecast_rows = []

    for future_date in future_dates:
        future_row = {}

        future_row["YEAR"] = future_date.year
        future_row["MONTH_NUMBER"] = future_date.month
        future_row["QUARTER"] = future_date.quarter
        future_row["TIME_INDEX"] = next_time_index

        for column in ECONOMIC_COLUMNS:
            future_row[column] = float(last_known_row[column])

        future_row["PRICE_LAG_1"] = price_history[-1]
        future_row["PRICE_LAG_3"] = price_history[-3]
        future_row["PRICE_LAG_6"] = price_history[-6]
        future_row["PRICE_LAG_12"] = price_history[-12]

        future_row["PRICE_ROLLING_MEAN_3"] = (
            sum(price_history[-3:]) / 3
        )

        future_row["PRICE_ROLLING_MEAN_6"] = (
            sum(price_history[-6:]) / 6
        )

        future_row["PRICE_ROLLING_MEAN_12"] = (
            sum(price_history[-12:]) / 12
        )

        X_future = pd.DataFrame(
            [future_row],
            columns=feature_columns,
        )

        predicted_price = float(
            model.predict(X_future)[0]
        )

        forecast_rows.append({
            "DATE": future_date,
            "YEAR": future_date.year,
            "MONTH_NUMBER": future_date.month,
            "PREDICTED_PRICE_USD": round(
                predicted_price,
                2,
            ),
        })

        # The new prediction becomes part of the history
        # for the following month's lag features.
        price_history.append(predicted_price)

        next_time_index += 1

    forecast_df = pd.DataFrame(forecast_rows)

    reports_folder = Path("reports")
    reports_folder.mkdir(exist_ok=True)

    output_path = reports_folder / "phosphate_price_forecast_2030.csv"

    forecast_df.to_csv(
        output_path,
        index=False,
    )

    print("\n===== FORECAST PERIOD =====")
    print(f"Start: {future_dates.min().date()}")
    print(f"End: {future_dates.max().date()}")
    print(f"Forecasted months: {len(forecast_df)}")

    print("\n===== FIRST FORECASTS =====")
    print(forecast_df.head())

    print("\n===== LAST FORECASTS =====")
    print(forecast_df.tail())

    print(f"\nForecast saved to: {output_path}")


if __name__ == "__main__":
    main()