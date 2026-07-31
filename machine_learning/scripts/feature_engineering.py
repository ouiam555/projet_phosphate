import pandas as pd

from load_data import load_data

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = df.sort_values(["YEAR", "MONTH_NUMBER"]).reset_index(drop=True)

    df["TOTAL_RESERVES_KTONS"] = (
        df["TOTAL_RESERVES_KTONS"]
        .interpolate()
        .bfill()
        .ffill()
    )

    df["DATE"] = pd.to_datetime(
        dict(
            year=df["YEAR"],
            month=df["MONTH_NUMBER"],
            day=1,
        )
    )

    df["QUARTER"] = df["DATE"].dt.quarter
    df["TIME_INDEX"] = range(len(df))

    df["PRICE_LAG_1"] = df["PHOSPHATE_PRICE_USD"].shift(1)
    df["PRICE_LAG_3"] = df["PHOSPHATE_PRICE_USD"].shift(3)
    df["PRICE_LAG_6"] = df["PHOSPHATE_PRICE_USD"].shift(6)
    df["PRICE_LAG_12"] = df["PHOSPHATE_PRICE_USD"].shift(12)

    df["PRICE_ROLLING_MEAN_3"] = (
        df["PHOSPHATE_PRICE_USD"]
        .shift(1)
        .rolling(window=3)
        .mean()
    )

    df["PRICE_ROLLING_MEAN_6"] = (
        df["PHOSPHATE_PRICE_USD"]
        .shift(1)
        .rolling(window=6)
        .mean()
    )

    df["PRICE_ROLLING_MEAN_12"] = (
        df["PHOSPHATE_PRICE_USD"]
        .shift(1)
        .rolling(window=12)
        .mean()
    )

    df = df.dropna().reset_index(drop=True)

    return df


if __name__ == "__main__":
    df = load_data()
    ml_dataframe = create_features(dataframe)

    print("\nFeature engineering completed successfully.")
    print(f"Final shape: {ml_dataframe.shape}")

    print("\nColumns:")
    print(ml_dataframe.columns.tolist())

    print("\nFirst 5 rows:")
    print(ml_dataframe.head())

    print("\nMissing values:")
    print(ml_dataframe.isnull().sum())