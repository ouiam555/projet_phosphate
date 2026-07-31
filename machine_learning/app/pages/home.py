from pathlib import Path
import sys

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# =========================================================
# PATH CONFIGURATION
# =========================================================

APP_DIR = Path(__file__).resolve().parent.parent

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


# =========================================================
# PROJECT IMPORTS
# =========================================================

from utils.database import run_query

from utils.queries import (
    FORECAST_QUERY,
    HISTORICAL_PRICE_QUERY,
    HOME_KPIS_QUERY,
)

from utils.ui import (
    content_card,
    insight_card,
    kpi_card,
    page_header,
    plotly_dark_layout,
    section_title,
    technology_card,
)


# =========================================================
# LOAD DATA FROM SNOWFLAKE
# =========================================================

try:
    kpis_df = run_query(HOME_KPIS_QUERY)
    historical_df = run_query(HISTORICAL_PRICE_QUERY)
    forecast_df = run_query(FORECAST_QUERY)

except Exception as error:
    st.error(
        "Unable to load data from Snowflake. "
        "Please verify the connection and SQL queries."
    )

    st.exception(error)
    st.stop()


if kpis_df.empty:
    st.error("The Home KPI query returned no data.")
    st.stop()


kpis = kpis_df.iloc[0]


latest_price = (
    float(kpis["LATEST_PRICE"])
    if pd.notna(kpis["LATEST_PRICE"])
    else 0.0
)

countries_count = (
    int(kpis["COUNTRIES_COUNT"])
    if pd.notna(kpis["COUNTRIES_COUNT"])
    else 0
)

forecast_end_year = (
    int(kpis["FORECAST_END_YEAR"])
    if pd.notna(kpis["FORECAST_END_YEAR"])
    else 0
)

forecast_rows = (
    int(kpis["FORECAST_ROWS"])
    if pd.notna(kpis["FORECAST_ROWS"])
    else 0
)


# =========================================================
# PREPARE DATA TYPES
# =========================================================

if not historical_df.empty:
    historical_df["DATE"] = pd.to_datetime(
        historical_df["DATE"],
        errors="coerce",
    )

    historical_df["PHOSPHATE_PRICE_USD"] = pd.to_numeric(
        historical_df["PHOSPHATE_PRICE_USD"],
        errors="coerce",
    )

    historical_df = (
        historical_df
        .dropna(
            subset=[
                "DATE",
                "PHOSPHATE_PRICE_USD",
            ]
        )
        .sort_values("DATE")
        .reset_index(drop=True)
    )


if not forecast_df.empty:
    forecast_df["DATE"] = pd.to_datetime(
        forecast_df["DATE"],
        errors="coerce",
    )

    forecast_df["FORECAST_PRICE_USD"] = pd.to_numeric(
        forecast_df["FORECAST_PRICE_USD"],
        errors="coerce",
    )

    forecast_df = (
        forecast_df
        .dropna(
            subset=[
                "DATE",
                "FORECAST_PRICE_USD",
            ]
        )
        .sort_values("DATE")
        .reset_index(drop=True)
    )


# =========================================================
# PAGE HEADER
# =========================================================

page_header(
    title="Phosphate Market Analytics",
    subtitle=(
        "Global phosphate market intelligence, forecasting "
        "and business analytics platform."
    ),
)


# =========================================================
# KPI CARDS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card(
        icon="$",
        label="Latest benchmark price",
        value=f"{latest_price:,.2f} USD",
        note="Per metric ton",
    )

with col2:
    kpi_card(
        icon="🌐",
        label="Countries covered",
        value=f"{countries_count:,}",
        note="Global trade and production coverage",
    )

with col3:
    kpi_card(
        icon="📅",
        label="Forecast horizon",
        value=str(forecast_end_year),
        note=f"{forecast_rows} monthly projections",
    )

with col4:
    kpi_card(
        icon="🧠",
        label="Selected model",
        value="ARIMA",
        note="Validated with walk-forward testing",
    )


# =========================================================
# MARKET INTELLIGENCE SECTION
# =========================================================

section_title(
    title="Market Intelligence",
    description=(
        "Historical benchmark prices and "
        "future ARIMA projections."
    ),
)


left, right = st.columns([1.8, 1])


with left:
    if historical_df.empty and forecast_df.empty:
        st.warning(
            "No historical or forecast data is available."
        )

    else:
        figure = go.Figure()

        if not historical_df.empty:
            figure.add_trace(
                go.Scatter(
                    x=historical_df["DATE"],
                    y=historical_df[
                        "PHOSPHATE_PRICE_USD"
                    ],
                    name="Historical price",
                    mode="lines",
                    line={
                        "color": "#A855F7",
                        "width": 3,
                    },
                    hovertemplate=(
                        "Date: %{x|%b %Y}<br>"
                        "Historical price: "
                        "%{y:.2f} USD/MT"
                        "<extra></extra>"
                    ),
                )
            )

        if not forecast_df.empty:
            figure.add_trace(
                go.Scatter(
                    x=forecast_df["DATE"],
                    y=forecast_df[
                        "FORECAST_PRICE_USD"
                    ],
                    name="ARIMA forecast",
                    mode="lines",
                    line={
                        "color": "#C084FC",
                        "width": 3,
                        "dash": "dash",
                    },
                    hovertemplate=(
                        "Date: %{x|%b %Y}<br>"
                        "Forecast: %{y:.2f} USD/MT"
                        "<extra></extra>"
                    ),
                )
            )

        if (
            not historical_df.empty
            and not forecast_df.empty
        ):
            forecast_start = forecast_df["DATE"].min()

            figure.add_vline(
                x=forecast_start,
                line_dash="dash",
                line_color="#94A3B8",
                opacity=0.75,
            )

            figure.add_annotation(
                x=forecast_start,
                y=historical_df[
                    "PHOSPHATE_PRICE_USD"
                ].max(),
                text="Forecast starts",
                showarrow=False,
                xanchor="left",
                font={
                    "color": "#C4B5FD",
                    "size": 12,
                },
            )

        plotly_dark_layout(
            figure=figure,
            title=(
                "Phosphate Price — "
                "Historical vs Forecast"
            ),
            height=480,
        )

        figure.update_layout(
            hovermode="x unified",
        )

        figure.update_xaxes(
            title="Date",
        )

        figure.update_yaxes(
            title="USD / Metric Ton",
            rangemode="tozero",
        )

        st.plotly_chart(
            figure,
            use_container_width=True,
            config={
                "displayModeBar": False,
            },
        )


with right:
    content_card(
        title="Market Summary",
        text=(
            "<b>Production</b>: global phosphate "
            "output by country and year.<br><br>"
            "<b>Exports</b>: reporter, partner, "
            "weight and trade-value analysis.<br><br>"
            "<b>Imports</b>: international demand "
            "and partner-country analysis.<br><br>"
            "<b>Inflation</b>: macroeconomic "
            "indicators by country and year."
        ),
        allow_html=True,
    )

    insight_card(
        title="Structural market break",
        text=(
            "The public benchmark contract price "
            "changed sharply around late 2023. "
            "Long-term forecasts should therefore "
            "be interpreted carefully."
        ),
        icon="⚠",
    )


# =========================================================
# PLATFORM INFORMATION
# =========================================================

section_title(
    title="Platform Architecture",
    description=(
        "Automated data engineering, analytics "
        "and machine-learning workflow."
    ),
)


bottom1, bottom2 = st.columns([1.05, 1.35])

with bottom1:
    content_card(
        title="Analytics Platform",
        text=(
            "Raw files and APIs are ingested into "
            "MinIO, orchestrated with Apache Airflow, "
            "loaded into Snowflake and transformed "
            "with dbt into a Galaxy Schema."
        ),
    )

with bottom2:
    technology_card(
        [
            "Python",
            "Pandas",
            "Streamlit",
            "Plotly",
            "Snowflake",
            "dbt",
            "Apache Airflow",
            "Docker",
            "MinIO",
            "Power BI",
            "ARIMA",
            "Random Forest",
            "XGBoost",
            "Prophet",
        ]
    )