from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


APP_DIR = Path(__file__).resolve().parent.parent

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


from utils.ui import (
    kpi_card,
    page_header,
    plotly_dark_layout,
    section_title,
)


page_header(
    title="Market Analytics",
    subtitle=(
        "Historical price, production and international "
        "phosphate trade analysis."
    ),
)


# =========================================================
# KPIs
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card(
        icon="$",
        label="Latest price",
        value="152.50 USD",
        note="Benchmark contract price",
    )

with col2:
    kpi_card(
        icon="🏭",
        label="Top producer",
        value="China",
        note="Based on production volume",
    )

with col3:
    kpi_card(
        icon="🚢",
        label="Trade coverage",
        value="Global",
        note="Imports and exports",
    )

with col4:
    kpi_card(
        icon="📊",
        label="Analysis period",
        value="2016–2026",
        note="Historical market analysis",
    )


# =========================================================
# PRICE ANALYSIS
# =========================================================

section_title(
    title="Price and Production",
    description="Historical benchmark price and leading producers.",
)


price_df = pd.DataFrame(
    {
        "YEAR": list(range(2016, 2027)),
        "AVERAGE_PRICE": [
            110.0,
            91.0,
            88.0,
            87.0,
            76.0,
            116.0,
            258.0,
            333.0,
            152.5,
            152.5,
            152.5,
        ],
    }
)

production_df = pd.DataFrame(
    {
        "COUNTRY": [
            "China",
            "Morocco",
            "United States",
            "Russia",
            "Jordan",
        ],
        "PRODUCTION": [
            90,
            38,
            22,
            14,
            11,
        ],
    }
)


left, right = st.columns([1.45, 1])

with left:
    price_figure = go.Figure()

    price_figure.add_trace(
        go.Scatter(
            x=price_df["YEAR"],
            y=price_df["AVERAGE_PRICE"],
            mode="lines+markers",
            name="Average price",
            line={
                "color": "#A855F7",
                "width": 3,
            },
            marker={
                "color": "#D8B4FE",
                "size": 8,
            },
        )
    )

    plotly_dark_layout(
        figure=price_figure,
        title="Average Phosphate Price Over Time",
        height=470,
    )

    price_figure.update_yaxes(
        title="USD / Metric Ton"
    )

    st.plotly_chart(
        price_figure,
        use_container_width=True,
        config={
            "displayModeBar": False,
        },
    )

with right:
    production_figure = px.bar(
        production_df.sort_values(
            "PRODUCTION",
            ascending=True,
        ),
        x="PRODUCTION",
        y="COUNTRY",
        orientation="h",
        title="Top Phosphate Producers",
    )

    production_figure.update_traces(
        marker={
            "color": "#8B5CF6",
            "line": {
                "color": "#C084FC",
                "width": 1,
            },
        }
    )

    plotly_dark_layout(
        figure=production_figure,
        title="Top Phosphate Producers",
        height=470,
    )

    production_figure.update_xaxes(
        title="Production"
    )

    production_figure.update_yaxes(
        title=""
    )

    st.plotly_chart(
        production_figure,
        use_container_width=True,
        config={
            "displayModeBar": False,
        },
    )


# =========================================================
# TRADE ANALYSIS
# =========================================================

section_title(
    title="International Trade",
    description="Comparison between total import and export values.",
)


trade_df = pd.DataFrame(
    {
        "YEAR": list(range(2016, 2027)),
        "EXPORT_VALUE": [
            7.2,
            7.8,
            8.1,
            7.9,
            7.1,
            8.8,
            11.6,
            12.9,
            12.4,
            12.5,
            12.6,
        ],
        "IMPORT_VALUE": [
            6.9,
            7.1,
            7.4,
            7.2,
            6.8,
            8.0,
            10.5,
            11.8,
            11.3,
            11.4,
            11.5,
        ],
    }
)


trade_figure = go.Figure()

trade_figure.add_trace(
    go.Bar(
        x=trade_df["YEAR"],
        y=trade_df["EXPORT_VALUE"],
        name="Exports",
        marker_color="#8B5CF6",
    )
)

trade_figure.add_trace(
    go.Bar(
        x=trade_df["YEAR"],
        y=trade_df["IMPORT_VALUE"],
        name="Imports",
        marker_color="#38BDF8",
    )
)

trade_figure.update_layout(
    barmode="group"
)

plotly_dark_layout(
    figure=trade_figure,
    title="Import vs Export Value",
    height=430,
)

trade_figure.update_yaxes(
    title="Value — Billion USD"
)

st.plotly_chart(
    trade_figure,
    use_container_width=True,
    config={
        "displayModeBar": False,
    },
)