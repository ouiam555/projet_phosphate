import math
import pandas as pd

from prophet import Prophet

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error,
)

from load_data import load_data


def main():

    df = load_data()

    prophet_df = df[
        ["YEAR", "MONTH_NUMBER", "PHOSPHATE_PRICE_USD"]
    ].copy()

    prophet_df["ds"] = pd.to_datetime(
        prophet_df["YEAR"].astype(str)
        + "-"
        + prophet_df["MONTH_NUMBER"].astype(str).str.zfill(2)
        + "-01"
    )

    prophet_df = prophet_df.rename(
        columns={
            "PHOSPHATE_PRICE_USD": "y"
        }
    )

    prophet_df = prophet_df[["ds", "y"]]

    train = prophet_df.iloc[:-12].copy()
    test = prophet_df.iloc[-12:].copy()

    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False,
    )

    model.fit(train)

    future = model.make_future_dataframe(
        periods=12,
        freq="MS"
    )

    forecast = model.predict(future)

    predictions = forecast.tail(12).copy()

    mae = mean_absolute_error(
        test["y"],
        predictions["yhat"]
    )

    import math

    mse = mean_squared_error(
    test["y"],
    predictions["yhat"]
)

    rmse = math.sqrt(mse)

    mape = mean_absolute_percentage_error(
        test["y"],
        predictions["yhat"]
    ) * 100

    print("\n===== PROPHET EVALUATION =====")
    print(f"Training rows : {len(train)}")
    print(f"Testing rows  : {len(test)}")

    print(f"\nMAE  : {mae:.2f}")
    print(f"RMSE : {rmse:.2f}")
    print(f"MAPE : {mape:.2f}%")

    results = pd.DataFrame({
        "DATE": test["ds"].values,
        "REAL": test["y"].values,
        "PREDICTED": predictions["yhat"].values,
    })

    print("\n===== REAL VS PREDICTED =====")
    print(results)

    results.to_csv(
        "reports/prophet_evaluation.csv",
        index=False
    )


if __name__ == "__main__":
    main()