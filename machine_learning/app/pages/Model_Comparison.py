import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


APP_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(APP_DIR))

from utils.ui import load_css, page_header


st.set_page_config(
    page_title="Model Comparison",
    page_icon="📋",
    layout="wide",
)

load_css()

page_header(
    "Model Comparison",
    "Comparison of regression, ensemble and time-series models.",
)

models = pd.DataFrame(
    {
        "Model": [
            "ARIMA",
            "Random Forest",
            "XGBoost",
            "Linear Regression",
            "Prophet",
        ],
        "MAE": [
            0.13,
            0.63,
            1.58,
            41.36,
            86.18,
        ],
        "RMSE": [
            0.14,
            0.96,
            3.90,
            43.62,
            86.45,
        ],
    }
)

left, right = st.columns([1, 1.4])

with left:
    st.dataframe(
        models,
        use_container_width=True,
        hide_index=True,
    )

with right:
    fig = px.bar(
        models,
        x="Model",
        y="MAE",
        title="MAE by model",
    )

    fig.update_traces(
        marker_color="#8B5CF6"
    )

    fig.update_layout(
        paper_bgcolor="#0F1A2C",
        plot_bgcolor="#0F1A2C",
        font_color="#F8FAFC",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

st.warning(
    "The low ARIMA error is associated with the stable-price test period. "
    "Walk-forward validation showed significantly weaker performance during "
    "rapid market changes."
)