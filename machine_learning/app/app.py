from pathlib import Path
import sys

import streamlit as st


APP_DIR = Path(__file__).resolve().parent

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from utils.ui import load_css, render_sidebar_brand


st.set_page_config(
    page_title="Phosphate Market Analytics",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)


load_css()


home_page = st.Page(
    "pages/home.py",
    title="Home",
    icon=":material/home:",
    default=True,
)

data_page = st.Page(
    "pages/data_overview.py",
    title="Data Overview",
    icon=":material/database:",
)

market_page = st.Page(
    "pages/market_analytics.py",
    title="Market Analytics",
    icon=":material/monitoring:",
)

ml_page = st.Page(
    "pages/machine_learning.py",
    title="Machine Learning",
    icon=":material/psychology:",
)

forecast_page = st.Page(
    "pages/forecast.py",
    title="Forecast",
    icon=":material/track_changes:",
)

comparison_page = st.Page(
    "pages/model_comparison.py",
    title="Model Comparison",
    icon=":material/balance:",
)

about_page = st.Page(
    "pages/about.py",
    title="About",
    icon=":material/info:",
)


navigation = st.navigation(
    {
        "PHOSPHATE ANALYTICS": [
            home_page,
            data_page,
            market_page,
            ml_page,
            forecast_page,
            comparison_page,
            about_page,
        ]
    },
    position="sidebar",
)


render_sidebar_brand()

navigation.run()