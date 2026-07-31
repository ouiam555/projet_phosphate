import os

import pandas as pd
import snowflake.connector
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


def load_data() -> pd.DataFrame:
    connection = None

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

        query = """
        SELECT *
        FROM GOLD.VW_ML_PRICE_DATASET
        ORDER BY YEAR, MONTH_NUMBER
        """

        cursor = connection.cursor()

        try:
            cursor.execute(query)
            dataframe = cursor.fetch_pandas_all()
        finally:
            cursor.close()

        print("Data loaded successfully from Snowflake.")
        print(f"Shape: {dataframe.shape}")

        return dataframe

    except Exception as error:
        print(f"Error while loading data from Snowflake: {error}")
        raise

    finally:
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    df = load_data()

    print("\n========== FIRST 5 ROWS ==========")
    print(df.head())

    print("\n========== DATA TYPES ==========")
    print(df.dtypes)

    print("\n========== MISSING VALUES ==========")
    print(df.isnull().sum())

    print("\n========== DESCRIPTIVE STATISTICS ==========")
    print(df.describe())