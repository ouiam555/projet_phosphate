FROM apache/airflow:3.3.0

USER airflow

RUN pip install --no-cache-dir \
    dbt-core==1.12.0 \
    dbt-snowflake==1.12.0 \
    minio