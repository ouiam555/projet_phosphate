import os

import pandas as pd
from dotenv import load_dotenv
from snowflake.connector import connect
from snowflake.connector.pandas_tools import write_pandas

from ingestion.download.download_minio import download_file
# ==========================================
# Load Environment Variables
# ==========================================

load_dotenv()

conn = connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
    role=os.getenv("SNOWFLAKE_ROLE"),
)

cursor = conn.cursor()

cursor.execute(f"USE WAREHOUSE {os.getenv('SNOWFLAKE_WAREHOUSE')}")
cursor.execute(f"USE DATABASE {os.getenv('SNOWFLAKE_DATABASE')}")
cursor.execute(f"USE SCHEMA {os.getenv('SNOWFLAKE_SCHEMA')}")

# ==========================================
# Files stored in MinIO
# ==========================================

FILES = {
    "PRICE_RAW": "prices.csv",
    "PRODUCTION_RAW": "production.csv",
    "INFLATION_RAW": "inflation_2016_2026.csv",
    "IMPORT_RAW": "import_2016_2026.csv",
    "EXPORT_RAW": "export_2016_2026.csv",
}

# ==========================================
# Load each file
# ==========================================

for table_name, object_name in FILES.items():

    print("=" * 60)
    print(f"Loading {table_name}")

    # Download from MinIO
    local_file = download_file(object_name)

    # Read with Pandas
    df = pd.read_csv(local_file)

    print(df.shape)

    # Uppercase column names
    df.columns = [c.upper() for c in df.columns]

    # Infer Snowflake types
    columns = []

    for col, dtype in zip(df.columns, df.dtypes):

        if "int" in str(dtype):
            snow_type = "NUMBER"

        elif "float" in str(dtype):
            snow_type = "FLOAT"

        elif "bool" in str(dtype):
            snow_type = "BOOLEAN"

        else:
            snow_type = "VARCHAR"

        columns.append(f'"{col}" {snow_type}')

    create_sql = f"""
    CREATE OR REPLACE TABLE {table_name}
    (
        {', '.join(columns)}
    )
    """

    cursor.execute(create_sql)

    success, nchunks, nrows, _ = write_pandas(
        conn,
        df,
        table_name=table_name,
        quote_identifiers=False,
    )

    if success:
        print(f" {table_name}: {nrows} rows loaded")

    else:
        print(f" Error loading {table_name}")

cursor.close()
conn.close()

print("\n Bronze Layer loaded successfully.")