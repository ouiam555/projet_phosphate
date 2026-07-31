from pathlib import Path
import sys

import streamlit as st


APP_DIR = Path(__file__).resolve().parent.parent

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


from utils.ui import (
    content_card,
    page_header,
    section_title,
    technology_card,
)


page_header(
    title="About the Project",
    subtitle=(
        "End-to-end phosphate market analytics "
        "and forecasting platform."
    ),
)


# =========================================================
# PROJECT
# =========================================================

section_title(
    title="Project Overview",
    description="Business objective and analytical scope.",
)

content_card(
    title="Project Objective",
    text=(
        "Build a complete analytics platform covering data ingestion, "
        "transformation, data warehousing, business intelligence, "
        "machine learning and interactive forecasting."
    ),
)

content_card(
    title="Business Scope",
    text=(
        "The project analyzes phosphate prices, global production, "
        "imports, exports, reserves and inflation indicators between "
        "2016 and 2026."
    ),
)


# =========================================================
# ARCHITECTURE
# =========================================================

section_title(
    title="Technical Architecture",
    description="End-to-end data and analytics workflow.",
)

content_card(
    title="Architecture Flow",
    text=(
        "Raw CSV and APIs → MinIO Bronze → Apache Airflow → "
        "Snowflake Bronze / Silver / Gold → dbt transformations → "
        "Galaxy Schema → Machine Learning → Streamlit and Power BI."
    ),
)

content_card(
    title="Machine-learning Workflow",
    text=(
        "Data loading from Snowflake → feature engineering → baseline → "
        "Linear Regression → Random Forest → XGBoost → Prophet → ARIMA → "
        "walk-forward validation → forecast export."
    ),
)


# =========================================================
# TECHNOLOGY
# =========================================================

section_title(
    title="Technology Stack",
    description="Tools used across the analytics platform.",
)

technology_card(
    [
        "Python",
        "Pandas",
        "Scikit-learn",
        "XGBoost",
        "Statsmodels",
        "Prophet",
        "Streamlit",
        "Plotly",
        "Snowflake",
        "dbt",
        "Airflow",
        "Docker",
        "MinIO",
        "Power BI",
    ]
)


# =========================================================
# AUTHOR
# =========================================================

section_title(
    title="Author",
    description="Portfolio project information.",
)

content_card(
    title="Ouiam El Khalfi",
    text=(
        "Developed as an end-to-end Data Analytics and Data Engineering "
        "portfolio project, combining business analysis, cloud data "
        "warehousing, automation, visualization and machine learning."
    ),
)