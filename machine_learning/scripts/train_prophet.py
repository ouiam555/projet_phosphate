from prophet import Prophet

from load_data import load_data


def main():

    df = load_data()

    prophet_df = df[["YEAR", "MONTH_NUMBER", "PHOSPHATE_PRICE_USD"]].copy()

    prophet_df["ds"] = (
        prophet_df["YEAR"].astype(str)
        + "-"
        + prophet_df["MONTH_NUMBER"].astype(str).str.zfill(2)
        + "-01"
    )

    prophet_df["ds"] = prophet_df["ds"].astype("datetime64[ns]")

    prophet_df = prophet_df.rename(
        columns={
            "PHOSPHATE_PRICE_USD": "y"
        }
    )

    prophet_df = prophet_df[["ds", "y"]]

    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False,
    )

    model.fit(prophet_df)

    future = model.make_future_dataframe(
        periods=120,
        freq="MS",
    )

    forecast = model.predict(future)

    print("\n===== LAST FORECASTS =====")

    print(
        forecast[
            ["ds", "yhat", "yhat_lower", "yhat_upper"]
        ].tail(20)
    )

    forecast[
        ["ds", "yhat", "yhat_lower", "yhat_upper"]
    ].to_csv(
        "reports/prophet_forecast.csv",
        index=False,
    )


if __name__ == "__main__":
    main()