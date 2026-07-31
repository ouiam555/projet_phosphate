from html import escape
from pathlib import Path

import streamlit as st


APP_DIR = Path(__file__).resolve().parent.parent


def load_css() -> None:
    """
    Load the shared CSS file used by all Streamlit pages.
    """

    css_path = APP_DIR / "assets" / "style.css"

    if not css_path.exists():
        raise FileNotFoundError(
            f"CSS file not found: {css_path}"
        )

    css_content = css_path.read_text(
        encoding="utf-8"
    )

    st.html(
        f"<style>{css_content}</style>"
    )


def render_sidebar_brand() -> None:
    """
    Render the project brand, Snowflake status,
    and footer inside the sidebar.
    """

    with st.sidebar:
        st.html(
            '<div class="sidebar-brand">'
            '<div class="brand-logo">◆</div>'
            '<div>'
            '<div class="brand-name">'
            'Phosphate Analytics'
            '</div>'
            '<div class="brand-subtitle">'
            'Market intelligence platform'
            '</div>'
            '</div>'
            '</div>'
        )

        st.html(
            '<div class="sidebar-status-card">'
            '<div class="status-label">'
            'DATA SOURCE'
            '</div>'
            '<div class="status-value">'
            '❄ Snowflake GOLD layer'
            '</div>'
            '<div class="connected-status">'
            '● Connected'
            '</div>'
            '<div class="status-separator"></div>'
            '<div class="status-label">'
            'LAST UPDATE'
            '</div>'
            '<div class="status-value">'
            'Pipeline-managed refresh'
            '</div>'
            '</div>'
        )

        st.html(
            '<div class="sidebar-footer">'
            '© 2026 Phosphate Analytics<br>'
            'All rights reserved'
            '</div>'
        )


def page_header(
    title: str,
    subtitle: str,
    icon: str = "",
) -> None:
    """
    Render the main title and subtitle of a page.
    """

    safe_title = escape(title)
    safe_subtitle = escape(subtitle)
    safe_icon = escape(icon)

    st.html(
        '<div class="hero-header">'
        '<div>'
        f'<div class="page-title">'
        f'{safe_icon} {safe_title} '
        '<span class="title-star">✦</span>'
        '</div>'
        f'<div class="page-subtitle">'
        f'{safe_subtitle}'
        '</div>'
        '</div>'
        '<div class="live-badge">'
        '<span class="live-dot"></span>'
        'LIVE ANALYTICS'
        '</div>'
        '</div>'
    )


def kpi_card(
    icon: str,
    label: str,
    value: str,
    note: str,
    delta: str | None = None,
    delta_type: str = "positive",
) -> None:
    """
    Render a KPI card.

    delta_type accepts:
    - positive
    - negative
    """

    safe_icon = escape(icon)
    safe_label = escape(label)
    safe_value = escape(value)
    safe_note = escape(note)

    delta_html = ""

    if delta:
        safe_delta = escape(delta)

        css_class = (
            "negative"
            if delta_type == "negative"
            else "positive"
        )

        delta_html = (
            f'<div class="kpi-delta {css_class}">'
            f'{safe_delta}'
            '</div>'
        )

    st.html(
        '<div class="kpi-card">'
        '<div class="kpi-pattern"></div>'
        '<div class="kpi-content">'
        f'<div class="kpi-icon">'
        f'{safe_icon}'
        '</div>'
        '<div class="kpi-details">'
        f'<div class="kpi-label">'
        f'{safe_label}'
        '</div>'
        f'<div class="kpi-value">'
        f'{safe_value}'
        '</div>'
        f'<div class="kpi-note">'
        f'{safe_note}'
        '</div>'
        f'{delta_html}'
        '</div>'
        '</div>'
        '</div>'
    )


def section_title(
    title: str,
    description: str | None = None,
) -> None:
    """
    Render a section heading with a violet accent line.
    """

    safe_title = escape(title)
    description_html = ""

    if description:
        safe_description = escape(description)

        description_html = (
            '<div class="section-description">'
            f'{safe_description}'
            '</div>'
        )

    st.html(
        '<div class="section-heading">'
        '<div class="section-accent"></div>'
        '<div>'
        f'<div class="section-title">'
        f'{safe_title}'
        '</div>'
        f'{description_html}'
        '</div>'
        '</div>'
    )


def content_card(
    title: str,
    text: str,
    allow_html: bool = False,
) -> None:
    """
    Render a standard content card.

    Set allow_html=True only when the text contains
    trusted HTML such as <br> or <b>.
    """

    safe_title = escape(title)

    if allow_html:
        safe_text = text
    else:
        safe_text = escape(text)

    st.html(
        '<div class="content-card">'
        f'<div class="card-title">'
        f'{safe_title}'
        '</div>'
        f'<div class="card-text">'
        f'{safe_text}'
        '</div>'
        '</div>'
    )


def insight_card(
    title: str,
    text: str,
    icon: str = "✦",
) -> None:
    """
    Render a highlighted analytical insight card.
    """

    safe_title = escape(title)
    safe_text = escape(text)
    safe_icon = escape(icon)

    st.html(
        '<div class="insight-card">'
        f'<div class="insight-icon">'
        f'{safe_icon}'
        '</div>'
        '<div>'
        f'<div class="card-title">'
        f'{safe_title}'
        '</div>'
        f'<div class="card-text">'
        f'{safe_text}'
        '</div>'
        '</div>'
        '</div>'
    )


def technology_card(
    technologies: list[str],
) -> None:
    """
    Render the technology stack badges.
    """

    badges_html = "".join(
        (
            '<span class="tech-badge">'
            f'{escape(technology)}'
            '</span>'
        )
        for technology in technologies
    )

    st.html(
        '<div class="content-card">'
        '<div class="card-title">'
        'Technology Stack'
        '</div>'
        f'{badges_html}'
        '</div>'
    )


def plotly_dark_layout(
    figure,
    title: str | None = None,
    height: int = 440,
):
    """
    Apply the common dark-violet layout to Plotly charts.
    """

    figure.update_layout(
        title=title,
        height=height,
        paper_bgcolor="#0C1728",
        plot_bgcolor="#0C1728",
        font=dict(
            color="#E9E7F7",
            family=(
                "Inter, Segoe UI, "
                "Arial, sans-serif"
            ),
        ),
        title_font=dict(
            color="#FFFFFF",
            size=18,
        ),
        margin=dict(
            l=35,
            r=25,
            t=60,
            b=40,
        ),
        hoverlabel=dict(
            bgcolor="#111C30",
            bordercolor="#8B5CF6",
            font_color="#FFFFFF",
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#D8D5EA"
            ),
        ),
        xaxis=dict(
            gridcolor=(
                "rgba(148,163,184,0.12)"
            ),
            zerolinecolor=(
                "rgba(148,163,184,0.15)"
            ),
        ),
        yaxis=dict(
            gridcolor=(
                "rgba(148,163,184,0.12)"
            ),
            zerolinecolor=(
                "rgba(148,163,184,0.15)"
            ),
        ),
    )

    return figure