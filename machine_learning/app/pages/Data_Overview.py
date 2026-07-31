from pathlib import Path
import sys

import pandas as pd
import streamlit as st


APP_DIR = Path(__file__).resolve().parent.parent

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


from utils.ui import (
    content_card,
    kpi_card,
    page_header,
    section_title,
)


page_header(
    title="Data Overview",
    subtitle=(
        "Global overview of the datasets available "
        "in the Snowflake GOLD layer."
    ),
)


# =========================================================
# KPI CARDS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card(
        icon="🗄️",
        label="Gold tables",
        value="9",
        note="Analytics-ready tables",
    )

with col2:
    kpi_card(
        icon="🌐",
        label="Countries",
        value="211",
        note="Global country coverage",
    )

with col3:
    kpi_card(
        icon="📅",
        label="Historical period",
        value="2016–2026",
        note="Monthly and yearly data",
    )

with col4:
    kpi_card(
        icon="✅",
        label="Data completeness",
        value="99.8%",
        note="After Silver transformations",
    )


# =========================================================
# DATASETS
# =========================================================

section_title(
    title="Available Datasets",
    description="Core analytical datasets prepared in the GOLD layer.",
)


datasets = pd.DataFrame(
    {
        "Dataset": [
            "Prices",
            "Production",
            "Exports",
            "Imports",
            "Inflation",
            "Forecast",
        ],
        "Granularity": [
            "Monthly",
            "Country / Year",
            "Country / Month",
            "Country / Month",
            "Country / Year",
            "Monthly",
        ],
        "Snowflake Table": [
            "FACT_PRICE",
            "FACT_PRODUCTION",
            "FACT_EXPORT",
            "FACT_IMPORT",
            "FACT_INFLATION",
            "FACT_PRICE_FORECAST",
        ],
        "Layer": [
            "GOLD",
            "GOLD",
            "GOLD",
            "GOLD",
            "GOLD",
            "GOLD",
        ],
    }
)


left, right = st.columns([1.45, 1])

with left:
    st.dataframe(
        datasets,
        use_container_width=True,
        hide_index=True,
    )

with right:
    content_card(
        title="Data-quality Summary",
        text=(
            "✓ Standardized data types<br><br>"
            "✓ Duplicate records removed<br><br>"
            "✓ Missing values controlled<br><br>"
            "✓ Date keys standardized<br><br>"
            "✓ Galaxy schema implemented"
        ),
        allow_html=True,
    )


# =========================================================
# DATA PIPELINE
# =========================================================

section_title(
    title="Data Lifecycle",
    description="From raw source files to analytical data products.",
)

content_card(
    title="Pipeline Flow",
    text=(
        "CSV and API sources → MinIO Bronze storage → "
        "Airflow orchestration → Snowflake Bronze → "
        "dbt Silver transformations → GOLD Galaxy Schema → "
        "Machine Learning → Streamlit and Power BI."
    ),
)