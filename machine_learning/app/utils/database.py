import os

import pandas as pd
import snowflake.connector
import streamlit as st
from dotenv import load_dotenv


load_dotenv()


@st.cache_resource
def get_connection():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema="GOLD",
        role=os.getenv("SNOWFLAKE_ROLE"),
    )


@st.cache_data(ttl=600)
def run_query(query: str) -> pd.DataFrame:
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(query)
        return cursor.fetch_pandas_all()
    finally:
        cursor.close()