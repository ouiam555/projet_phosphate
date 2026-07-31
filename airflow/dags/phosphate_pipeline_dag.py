from datetime import datetime, timedelta

from airflow.sdk import DAG
from airflow.providers.smtp.notifications.smtp import send_smtp_notification
from airflow.providers.standard.operators.bash import BashOperator


# ==========================
# Email Notifications
# ==========================

failure_email = send_smtp_notification(
    to="elkhalfiouiam5@gmail.com",
    from_email="elkhalfiouiam5@gmail.com",
    subject="[FAILED] Phosphate Pipeline",
    html_content="""
        <h2 style="color:red;"> Phosphate Pipeline Failed</h2>

        <p><strong>DAG:</strong> {{ dag.dag_id }}</p>
        <p><strong>Task:</strong> {{ task_instance.task_id }}</p>
        <p><strong>Execution Date:</strong> {{ logical_date }}</p>

        <p>Please check the Airflow logs.</p>
    """,
    smtp_conn_id="smtp_default",
)

success_email = send_smtp_notification(
    to="elkhalfiouiam5@gmail.com",
    from_email="elkhalfiouiam5@gmail.com",
    subject="[SUCCESS] Phosphate Pipeline",
    html_content="""
        <h2 style="color:green;"> Phosphate Pipeline Completed Successfully</h2>

        <p><strong>DAG:</strong> {{ dag.dag_id }}</p>
        <p><strong>Execution Date:</strong> {{ logical_date }}</p>

        <p>All pipeline tasks completed successfully.</p>
    """,
    smtp_conn_id="smtp_default",
)


# ==========================
# Default Arguments
# ==========================

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "on_failure_callback": failure_email,
}


# ==========================
# DAG
# ==========================

with DAG(
    dag_id="phosphate_pipeline",
    description="Automated phosphate analytics pipeline",
    default_args=default_args,
    start_date=datetime(2026, 7, 23),
    schedule="0 1 * * *",
    catchup=False,
    max_active_runs=1,
    tags=["phosphate", "dbt", "snowflake"],
) as dag:

    check_project_files = BashOperator(
        task_id="check_project_files",
        bash_command="""
        set -e

        test -d /opt/project/data
        test -d /opt/project/data/raw
        test -d /opt/project/ingestion
        test -d /opt/project/dbt

        echo "All project folders are available."
        """,
    )

    validate_raw_files = BashOperator(
        task_id="validate_raw_files",
        bash_command="""
        set -e

        RAW_DIR="/opt/project/data/raw"

        test -f "$RAW_DIR/export_2016_2026.csv"
        test -f "$RAW_DIR/import_2016_2026.csv"
        test -f "$RAW_DIR/inflation_2016_2026.csv"
        test -f "$RAW_DIR/prices.csv"
        test -f "$RAW_DIR/production.csv"

        echo "All required RAW files are present."
        """,
    )

    validate_csv_quality = BashOperator(
        task_id="validate_csv_quality",
        bash_command="""
        set -e

        python /opt/project/ingestion/validate_files.py

        echo "CSV quality validation completed."
        """,
    )

    upload_to_minio = BashOperator(
        task_id="upload_to_minio",
        bash_command="""
        set -e

        python /opt/project/ingestion/upload/upload_to_minio.py

        echo "MinIO upload completed successfully."
        """,
    )

    load_to_snowflake = BashOperator(
        task_id="load_to_snowflake",
        bash_command="""
        set -e

        export PYTHONPATH=/opt/project

        python /opt/project/ingestion/loaders/load_to_snowflake.py

        echo "Snowflake Bronze load completed successfully."
        """,
    )

    run_dbt_build = BashOperator(
        task_id="run_dbt_build",
        bash_command="""
        set -e

        cd /opt/project/dbt
        dbt build --profiles-dir /home/airflow/.dbt

        echo "dbt build completed successfully."
        """,
        on_success_callback=success_email,
    )

    (
        check_project_files
        >> validate_raw_files
        >> validate_csv_quality
        >> upload_to_minio
        >> load_to_snowflake
        >> run_dbt_build
    )