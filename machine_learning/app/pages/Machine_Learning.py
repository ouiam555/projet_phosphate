from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st


APP_DIR = Path(__file__).resolve().parent.parent

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


from utils.ui import (
    content_card,
    kpi_card,
    page_header,
    plotly_dark_layout,
    section_title,
)


page_header(
    title="Machine Learning",
    subtitle=(
        "Model training, evaluation, explainability "
        "and time-series validation."
    ),
)


# =========================================================
# KPI CARDS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card(
        icon="🏆",
        label="Best stable-regime model",
        value="ARIMA",
        note="MAE: 0.13 USD",
    )

with col2:
    kpi_card(
        icon="🌲",
        label="Best ML model",
        value="Random Forest",
        note="MAE: 0.63 USD",
    )

with col3:
    kpi_card(
        icon="🧪",
        label="Models evaluated",
        value="5",
        note="Regression and time-series",
    )

with col4:
    kpi_card(
        icon="⚠️",
        label="Structural break",
        value="Late 2023",
        note="Major price-regime change",
        delta="High model uncertainty",
        delta_type="negative",
    )


# =========================================================
# FEATURE IMPORTANCE
# =========================================================

section_title(
    title="Feature Importance",
    description=(
        "Variables with the strongest influence "
        "on the Random Forest model."
    ),
)


feature_df = pd.DataFrame(
    {
        "Feature": [
            "Price Lag 1",
            "Time Index",
            "Rolling Mean 3",
            "Inflation",
            "Import Weight",
            "Price Lag 3",
            "Month Number",
        ],
        "Importance": [
            0.796,
            0.072,
            0.065,
            0.018,
            0.018,
            0.009,
            0.006,
        ],
    }
)


feature_figure = px.bar(
    feature_df.sort_values(
        "Importance",
        ascending=True,
    ),
    x="Importance",
    y="Feature",
    orientation="h",
)

feature_figure.update_traces(
    marker={
        "color": "#8B5CF6",
        "line": {
            "color": "#C084FC",
            "width": 1,
        },
    }
)

plotly_dark_layout(
    figure=feature_figure,
    title="Random Forest Feature Importance",
    height=470,
)

feature_figure.update_xaxes(
    tickformat=".0%"
)

feature_figure.update_yaxes(
    title=""
)

st.plotly_chart(
    feature_figure,
    use_container_width=True,
    config={
        "displayModeBar": False,
    },
)


# =========================================================
# WALK-FORWARD VALIDATION
# =========================================================

section_title(
    title="Walk-Forward Validation",
    description="ARIMA performance across different market regimes.",
)


walk_forward_df = pd.DataFrame(
    {
        "Year": [
            2020,
            2021,
            2022,
            2023,
            2024,
            2025,
        ],
        "MAE": [
            6.56,
            38.30,
            44.69,
            45.91,
            165.46,
            0.23,
        ],
        "MAPE": [
            8.31,
            27.32,
            16.09,
            18.59,
            108.50,
            0.15,
        ],
    }
)


left, right = st.columns([1.4, 1])

with left:
    validation_figure = px.bar(
        walk_forward_df,
        x="Year",
        y="MAE",
        color="MAE",
        color_continuous_scale=[
            "#6D28D9",
            "#A855F7",
            "#FB7185",
        ],
    )

    plotly_dark_layout(
        figure=validation_figure,
        title="ARIMA MAE by Test Year",
        height=420,
    )

    validation_figure.update_coloraxes(
        showscale=False
    )

    st.plotly_chart(
        validation_figure,
        use_container_width=True,
        config={
            "displayModeBar": False,
        },
    )

with right:
    content_card(
        title="Interpretation",
        text=(
            "ARIMA performs very well during stable-price periods, "
            "but its performance deteriorates during sudden market shifts.<br><br>"
            "The 2024 structural break generated the highest forecasting error."
        ),
        allow_html=True,
    )