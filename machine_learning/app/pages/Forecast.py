from pathlib import Path
import sys

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


APP_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = APP_DIR.parent

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


from utils.ui import (
    content_card,
    kpi_card,
    page_header,
    plotly_dark_layout,
    section_title,
)


FORECAST_PATH = (
    PROJECT_DIR
    / "reports"
    / "forecast_price_2030.csv"
)


page_header(
    title="Price Forecast",
    subtitle=(
        "ARIMA phosphate benchmark-price projections "
        "with a 95% confidence interval."
    ),
)


if not FORECAST_PATH.exists():
    st.error(
        f"Forecast file not found: {FORECAST_PATH}"
    )
    st.stop()


forecast_df = pd.read_csv(
    FORECAST_PATH,
    parse_dates=["DATE"],
)

required_columns = {
    "DATE",
    "FORECAST_PRICE_USD",
    "LOWER_95",
    "UPPER_95",
}

missing_columns = (
    required_columns
    - set(forecast_df.columns)
)

if missing_columns:
    st.error(
        "Missing forecast columns: "
        + ", ".join(sorted(missing_columns))
    )
    st.stop()


forecast_df = (
    forecast_df
    .sort_values("DATE")
    .reset_index(drop=True)
)


# Display-only lower bound:
# negative prices are statistically possible in the raw
# confidence interval, but not economically interpretable.
forecast_df["DISPLAY_LOWER_95"] = (
    forecast_df["LOWER_95"]
    .clip(lower=0)
)


first_row = forecast_df.iloc[0]
last_row = forecast_df.iloc[-1]

forecast_months = len(forecast_df)

first_interval_width = (
    first_row["UPPER_95"]
    - first_row["LOWER_95"]
)

last_interval_width = (
    last_row["UPPER_95"]
    - last_row["LOWER_95"]
)


# =========================================================
# KPIs
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card(
        icon="📅",
        label="Forecast period",
        value=(
            f"{first_row['DATE']:%b %Y} "
            f"→ {last_row['DATE']:%b %Y}"
        ),
        note=f"{forecast_months} monthly projections",
    )

with col2:
    kpi_card(
        icon="$",
        label="Central forecast",
        value=(
            f"{first_row['FORECAST_PRICE_USD']:.2f} USD"
        ),
        note="First forecasted month",
    )

with col3:
    kpi_card(
        icon="↔",
        label="First-month 95% CI",
        value=(
            f"{first_row['LOWER_95']:.2f} "
            f"– {first_row['UPPER_95']:.2f}"
        ),
        note="USD per metric ton",
    )

with col4:
    kpi_card(
        icon="⚠️",
        label="Long-term uncertainty",
        value="Very high",
        note=(
            f"2030 interval width: "
            f"{last_interval_width:.2f} USD"
        ),
        delta="Interpret with caution",
        delta_type="negative",
    )


# =========================================================
# FORECAST CHART
# =========================================================

section_title(
    title="Forecast and Confidence Interval",
    description=(
        "The uncertainty band expands as the forecast "
        "moves further into the future."
    ),
)


figure = go.Figure()


# Upper confidence bound
figure.add_trace(
    go.Scatter(
        x=forecast_df["DATE"],
        y=forecast_df["UPPER_95"],
        mode="lines",
        line={
            "width": 0,
        },
        hoverinfo="skip",
        showlegend=False,
    )
)


# Lower confidence bound + fill
figure.add_trace(
    go.Scatter(
        x=forecast_df["DATE"],
        y=forecast_df["DISPLAY_LOWER_95"],
        mode="lines",
        line={
            "width": 0,
        },
        fill="tonexty",
        fillcolor="rgba(139, 92, 246, 0.18)",
        name="95% confidence interval",
        hovertemplate=(
            "Date: %{x|%b %Y}<br>"
            "Displayed lower bound: %{y:.2f}<extra></extra>"
        ),
    )
)


# Forecast line
figure.add_trace(
    go.Scatter(
        x=forecast_df["DATE"],
        y=forecast_df["FORECAST_PRICE_USD"],
        mode="lines+markers",
        name="ARIMA forecast",
        line={
            "color": "#C084FC",
            "width": 3,
        },
        marker={
            "size": 5,
            "color": "#E9D5FF",
        },
        hovertemplate=(
            "Date: %{x|%b %Y}<br>"
            "Forecast: %{y:.2f} USD/MT"
            "<extra></extra>"
        ),
    )
)


plotly_dark_layout(
    figure=figure,
    title="ARIMA Forecast Through 2030",
    height=570,
)

figure.update_yaxes(
    title="USD / Metric Ton",
    rangemode="tozero",
)

figure.update_xaxes(
    title="Forecast Month",
)

figure.update_layout(
    hovermode="x unified",
)


st.plotly_chart(
    figure,
    use_container_width=True,
    config={
        "displayModeBar": False,
    },
)


# =========================================================
# INTERPRETATION
# =========================================================

left, right = st.columns([1.2, 1])

with left:
    content_card(
        title="How to Read the Forecast",
        text=(
            "The central ARIMA estimate remains close to "
            "152.50 USD per metric ton. However, the confidence "
            "interval expands significantly with each additional "
            "forecast month, indicating rapidly increasing uncertainty."
        ),
    )

with right:
    content_card(
        title="Statistical Limitation",
        text=(
            "The raw lower confidence bound becomes negative "
            "over the long-term horizon. Negative commodity prices "
            "are not economically interpreted here; they indicate "
            "that the model is unsuitable for precise long-term "
            "decision-making under structural market change."
        ),
    )


# =========================================================
# FORECAST TABLE
# =========================================================

section_title(
    title="Forecast Table",
    description="Monthly central estimates and raw statistical bounds.",
)


table_df = forecast_df[
    [
        "DATE",
        "FORECAST_PRICE_USD",
        "LOWER_95",
        "UPPER_95",
    ]
].copy()

table_df["DATE"] = (
    table_df["DATE"]
    .dt.strftime("%Y-%m-%d")
)


st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=True,
)


csv_data = forecast_df[
    [
        "DATE",
        "YEAR",
        "MONTH_NUMBER",
        "FORECAST_PRICE_USD",
        "LOWER_95",
        "UPPER_95",
    ]
].to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="Download Forecast with 95% CI",
    data=csv_data,
    file_name="phosphate_price_forecast_2030_with_ci.csv",
    mime="text/csv",
    use_container_width=True,
)