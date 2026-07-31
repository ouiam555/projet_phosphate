import os
from pathlib import Path

import pandas as pd
import snowflake.connector
from dotenv import load_dotenv


load_dotenv()


def main() -> None:
    csv_path = Path("reports/forecast_price_2030.csv")

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Forecast file not found: {csv_path}"
        )

    df = pd.read_csv(
        csv_path,
        parse_dates=["DATE"],
    )

    df["MODEL_NAME"] = "ARIMA(2,1,2)"

    connection = None
    cursor = None

    try:
        connection = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema="GOLD",
            role=os.getenv("SNOWFLAKE_ROLE"),
        )

        cursor = connection.cursor()

        # Avoid duplicate forecasts when rerunning the script
        cursor.execute(
            """
            DELETE FROM GOLD.FACT_PRICE_FORECAST
            WHERE MODEL_NAME = 'ARIMA(2,1,2)'
            """
        )

        insert_query = """
            INSERT INTO GOLD.FACT_PRICE_FORECAST (
                DATE,
                YEAR,
                MONTH_NUMBER,
                FORECAST_PRICE_USD,
                MODEL_NAME
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        rows = [
            (
                row.DATE.to_pydatetime(),
                int(row.YEAR),
                int(row.MONTH_NUMBER),
                float(row.FORECAST_PRICE_USD),
                row.MODEL_NAME,
            )
            for row in df.itertuples(index=False)
        ]

        cursor.executemany(
            insert_query,
            rows,
        )

        connection.commit()

        print("\n===== FORECAST UPLOAD COMPLETED =====")
        print(f"Rows inserted: {len(rows)}")
        print("Target: GOLD.FACT_PRICE_FORECAST")

    except Exception as error:
        if connection is not None:
            connection.rollback()

        print(f"Upload failed: {error}")
        raise

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


if __name__ == "__main__":
    main()