"""
Theme system — Navy/Teal dual-theme.
Asset management aesthetic: institutional trust, modern precision.

Light: White base, navy text, teal accent, medium-navy sidebar, teal canvas
Dark:  Deep navy base, light text, bright teal accent, deep-teal canvas
"""

import streamlit as st

# ── Color Palettes ──────────────────────────────────────────────────────
LIGHT = {
    "bg": "#FFFFFF",
    "surface": "#F6F8FA",
    "card_bg": "rgba(246, 248, 250, 0.75)",
    "card_border": "rgba(13, 148, 136, 0.12)",
    "card_shadow": "0 2px 12px rgba(0, 0, 0, 0.04)",
    "text": "#0F1B2D",
    "text_muted": "#5A6B7F",
    "accent": "#0D9488",
    "accent_hover": "#0F766E",
    "accent_light": "rgba(13, 148, 136, 0.08)",
    "gradient": "linear-gradient(135deg, #0D9488 0%, #0891B2 100%)",
    "gold": "#B8860B",
    # Sidebar
    "sidebar_bg": "#1E3A5F",
    "sidebar_text": "#E8EDF2",
    "sidebar_heading": "#FFFFFF",
    "sidebar_muted": "#A3BFDB",
    "sidebar_divider": "rgba(255, 255, 255, 0.15)",
    # Guide card
    "guide_bg": "rgba(45, 212, 191, 0.12)",
    "guide_border": "#2DD4BF",
    "guide_text": "#E8EDF2",
    # Step badge
    "step_badge_bg": "rgba(13, 148, 136, 0.10)",
    "step_badge_text": "#0D9488",
    # Metrics
    "metric_bg": "rgba(13, 148, 136, 0.05)",
    "metric_border": "rgba(13, 148, 136, 0.12)",
    "divider": "#E5E8EB",
    "input_bg": "#FFFFFF",
    "input_border": "#D1D5DB",
    # Canvas — solid teal
    "canvas_bg": "#0D9488",
    "canvas_text": "#FFFFFF",
    "canvas_muted": "rgba(255,255,255,0.70)",
    "canvas_border": "rgba(255,255,255,0.15)",
    "canvas_surface": "rgba(255,255,255,0.08)",
    "canvas_metric_val": "#FFFFFF",
}

DARK = {
    "bg": "#0A1628",
    "surface": "#0F1F35",
    "card_bg": "rgba(15, 31, 53, 0.75)",
    "card_border": "rgba(45, 212, 191, 0.12)",
    "card_shadow": "0 2px 16px rgba(0, 0, 0, 0.25)",
    "text": "#E2E8F0",
    "text_muted": "#8B9DB5",
    "accent": "#2DD4BF",
    "accent_hover": "#5EEAD4",
    "accent_light": "rgba(45, 212, 191, 0.10)",
    "gradient": "linear-gradient(135deg, #2DD4BF 0%, #22D3EE 100%)",
    "gold": "#D4A574",
    # Sidebar
    "sidebar_bg": "#132A43",
    "sidebar_text": "#D1DBE8",
    "sidebar_heading": "#F0F4F8",
    "sidebar_muted": "#7A94B0",
    "sidebar_divider": "rgba(255, 255, 255, 0.10)",
    # Guide card
    "guide_bg": "rgba(45, 212, 191, 0.10)",
    "guide_border": "#2DD4BF",
    "guide_text": "#D1DBE8",
    # Step badge
    "step_badge_bg": "rgba(45, 212, 191, 0.12)",
    "step_badge_text": "#2DD4BF",
    # Metrics
    "metric_bg": "rgba(45, 212, 191, 0.06)",
    "metric_border": "rgba(45, 212, 191, 0.15)",
    "divider": "rgba(255, 255, 255, 0.06)",
    "input_bg": "#162236",
    "input_border": "rgba(255, 255, 255, 0.10)",
    # Canvas — deep teal
    "canvas_bg": "#0A4F4A",
    "canvas_text": "#E2F5F3",
    "canvas_muted": "rgba(226,245,243,0.60)",
    "canvas_border": "rgba(255,255,255,0.10)",
    "canvas_surface": "rgba(255,255,255,0.06)",
    "canvas_metric_val": "#2DD4BF",
}


def _build_css(t: dict) -> str:
    """Build the full CSS string from a theme palette."""
    return f"""
<style>
    /* ═══════════════════════════════════════════════════
       DATA PRODUCT BUILDER — THEME
       ═══════════════════════════════════════════════════ */

    /* ── App background ─────────────────────────────── */
    .stApp {{
        background: {t["bg"]};
        color: {t["text"]};
    }}

    /* ── Kill top whitespace ────────────────────────── */
    .main .block-container {{
        padding: 0.75rem 1.5rem 2rem 1.5rem;
        max-width: 100%;
    }}
    [data-testid="stHeader"] {{
        background: transparent;
        height: 0 !important;
        min-height: 0 !important;
    }}

    /* ── Base typography — larger ────────────────────── */
    [data-testid="stAppViewContainer"] > .main {{
        font-size: 1.15rem;
        line-height: 1.7;
        color: {t["text"]};
    }}
    h1 {{
        font-size: 2rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
        color: {t["text"]} !important;
        margin-bottom: 0 !important;
    }}
    h2 {{
        font-size: 1.6rem !important;
        font-weight: 600 !important;
        color: {t["text"]} !important;
    }}
    h3 {{
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        color: {t["text"]} !important;
    }}

    /* ── Markdown text ──────────────────────────────── */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {{
        color: {t["text"]};
        font-size: 1.12rem;
    }}
    [data-testid="stMarkdownContainer"] strong {{
        color: {t["text"]};
    }}
    .stCaption, [data-testid="stCaptionContainer"] {{
        color: {t["text_muted"]} !important;
        font-size: 0.95rem !important;
    }}

    /* ── Form labels ────────────────────────────────── */
    .stTextInput label p,
    .stSelectbox label p,
    .stMultiSelect label p,
    .stTextArea label p,
    .stSlider label p,
    .stNumberInput label p,
    .stCheckbox label p {{
        font-size: 1.08rem !important;
        font-weight: 500 !important;
        color: {t["text"]} !important;
    }}

    /* ── Inputs ─────────────────────────────────────── */
    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {{
        background: {t["input_bg"]} !important;
        border: 1px solid {t["input_border"]} !important;
        border-radius: 0.5rem !important;
        color: {t["text"]} !important;
        font-size: 1.05rem !important;
    }}
    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stNumberInput input:focus {{
        border-color: {t["accent"]} !important;
        box-shadow: 0 0 0 2px {t["accent_light"]} !important;
    }}

    /* ── Select boxes ───────────────────────────────── */
    .stSelectbox [data-baseweb="select"],
    .stMultiSelect [data-baseweb="select"] {{
        background: {t["input_bg"]} !important;
        border-color: {t["input_border"]} !important;
    }}
    .stSelectbox [data-baseweb="select"] > div,
    .stMultiSelect [data-baseweb="select"] > div {{
        background: {t["input_bg"]} !important;
        color: {t["text"]} !important;
    }}

    /* ── Metric cards ───────────────────────────────── */
    [data-testid="stMetric"] {{
        background: {t["card_bg"]};
        backdrop-filter: blur(12px);
        padding: 0.85rem 1rem;
        border-radius: 0.75rem;
        border: 1px solid {t["metric_border"]};
        box-shadow: {t["card_shadow"]};
    }}
    [data-testid="stMetric"] label {{
        color: {t["text_muted"]} !important;
        font-size: 0.9rem !important;
    }}
    [data-testid="stMetric"] [data-testid="stMetricValue"] {{
        color: {t["accent"]} !important;
        font-weight: 700 !important;
    }}

    /* ── Progress bar ───────────────────────────────── */
    .stProgress > div > div > div {{
        background: {t["gradient"]} !important;
    }}
    .stProgress > div > div {{
        background: {t["accent_light"]} !important;
    }}

    /* ═══════════════════════════════════════════════════
       SIDEBAR
       ═══════════════════════════════════════════════════ */
    section[data-testid="stSidebar"] {{
        background: {t["sidebar_bg"]} !important;
        font-size: 1.08rem;
    }}
    section[data-testid="stSidebar"] * {{
        color: {t["sidebar_text"]} !important;
    }}
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: {t["sidebar_heading"]} !important;
    }}
    section[data-testid="stSidebar"] h1 {{
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }}
    section[data-testid="stSidebar"] h3 {{
        font-size: 1.2rem !important;
        font-weight: 600 !important;
    }}
    section[data-testid="stSidebar"] .stCaption *,
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {{
        color: {t["sidebar_muted"]} !important;
    }}
    section[data-testid="stSidebar"] hr {{
        border-color: {t["sidebar_divider"]} !important;
    }}
    section[data-testid="stSidebar"] .streamlit-expanderHeader p {{
        color: {t["sidebar_text"]} !important;
        font-size: 1.08rem !important;
    }}
    section[data-testid="stSidebar"] .stToggle label span p {{
        color: {t["sidebar_text"]} !important;
        font-size: 1.08rem !important;
    }}
    section[data-testid="stSidebar"] .stProgress > div > div > div {{
        background: {t["gradient"]} !important;
    }}

    /* ── Guide card (sidebar) ───────────────────────── */
    .guide-card {{
        background: {t["guide_bg"]};
        border-left: 3px solid {t["guide_border"]};
        padding: 0.8rem;
        border-radius: 0 0.4rem 0.4rem 0;
        font-size: 1rem;
        line-height: 1.55;
        margin-bottom: 0.5rem;
    }}
    .guide-card, .guide-card * {{
        color: {t["guide_text"]} !important;
    }}

    /* ═══════════════════════════════════════════════════
       CANVAS RIGHT PANEL — solid teal
       ═══════════════════════════════════════════════════ */
    .canvas-panel {{
        background: {t["canvas_bg"]};
        border-radius: 0.75rem;
        padding: 1.25rem;
        min-height: 500px;
    }}
    .canvas-panel, .canvas-panel p, .canvas-panel li,
    .canvas-panel span, .canvas-panel strong, .canvas-panel b {{
        color: {t["canvas_text"]} !important;
    }}
    .canvas-panel .stCaption *,
    .canvas-panel [data-testid="stCaptionContainer"] * {{
        color: {t["canvas_muted"]} !important;
    }}
    .canvas-panel hr {{
        border-color: {t["canvas_border"]} !important;
    }}
    /* Metrics inside canvas */
    .canvas-panel [data-testid="stMetric"] {{
        background: {t["canvas_surface"]};
        border: 1px solid {t["canvas_border"]};
        box-shadow: none;
    }}
    .canvas-panel [data-testid="stMetric"] label {{
        color: {t["canvas_muted"]} !important;
    }}
    .canvas-panel [data-testid="stMetric"] [data-testid="stMetricValue"] {{
        color: {t["canvas_metric_val"]} !important;
    }}
    /* Downloads inside canvas */
    .canvas-panel .stDownloadButton button {{
        background: rgba(255,255,255,0.15) !important;
        color: {t["canvas_text"]} !important;
        border: 1px solid {t["canvas_border"]} !important;
    }}
    .canvas-panel .stDownloadButton button:hover {{
        background: rgba(255,255,255,0.25) !important;
    }}
    /* Expander inside canvas */
    .canvas-panel .streamlit-expanderHeader {{
        background: {t["canvas_surface"]} !important;
        color: {t["canvas_text"]} !important;
    }}
    .canvas-panel .streamlit-expanderHeader p {{
        color: {t["canvas_text"]} !important;
    }}

    /* ── Canvas header ──────────────────────────────── */
    .canvas-header {{
        color: {t["canvas_text"]} !important;
        font-weight: 700;
        font-size: 1.15rem;
        margin-bottom: 0.15rem;
        letter-spacing: -0.01em;
    }}
    .canvas-subtitle {{
        color: {t["canvas_muted"]} !important;
        font-size: 0.95rem;
        line-height: 1.5;
        margin-bottom: 0.75rem;
    }}
    .canvas-body {{
        background: {t["canvas_surface"]};
        border: 1px solid {t["canvas_border"]};
        border-radius: 0.5rem;
        padding: 0.8rem 1rem;
        font-size: 1rem;
        color: {t["canvas_text"]};
    }}

    /* ── Step badge ──────────────────────────────────── */
    .step-badge {{
        display: inline-block;
        background: {t["step_badge_bg"]};
        color: {t["step_badge_text"]};
        padding: 0.2rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
        letter-spacing: 0.02em;
    }}

    /* ── Expander ────────────────────────────────────── */
    .streamlit-expanderHeader {{
        background: {t["surface"]} !important;
        border-radius: 0.5rem !important;
        color: {t["text"]} !important;
    }}

    /* ── Tabs ────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: {t["text_muted"]} !important;
        border-radius: 0.5rem 0.5rem 0 0;
    }}
    .stTabs [aria-selected="true"] {{
        color: {t["accent"]} !important;
        border-bottom-color: {t["accent"]} !important;
    }}

    /* ── Code blocks ────────────────────────────────── */
    .stCodeBlock {{
        border-radius: 0.5rem !important;
    }}

    /* ── Alerts ──────────────────────────────────────── */
    .stAlert {{
        border-radius: 0.5rem !important;
    }}

    /* ── Dividers ────────────────────────────────────── */
    hr {{
        border-color: {t["divider"]} !important;
    }}

    /* ── Download buttons ────────────────────────────── */
    .stDownloadButton button {{
        background: {t["accent"]} !important;
        color: white !important;
        border: none !important;
        border-radius: 0.5rem !important;
        font-weight: 500 !important;
    }}
    .stDownloadButton button:hover {{
        background: {t["accent_hover"]} !important;
    }}

    /* ── Form submit button ──────────────────────────── */
    .stFormSubmitButton button {{
        background: {t["gradient"]} !important;
        color: white !important;
        border: none !important;
        border-radius: 0.5rem !important;
        font-weight: 600 !important;
        padding: 0.5rem 2rem !important;
    }}

    /* ── Regular buttons ─────────────────────────────── */
    .stButton > button {{
        border-color: {t["accent"]} !important;
        color: {t["accent"]} !important;
        border-radius: 0.5rem !important;
    }}
    .stButton > button:hover {{
        background: {t["accent_light"]} !important;
        border-color: {t["accent"]} !important;
        color: {t["accent"]} !important;
    }}

    /* ═══════════════════════════════════════════════════
       HOME — helpers ribbon, layout zones, journey
       ═══════════════════════════════════════════════════ */

    /* ── Helpers ribbon ─────────────────────────────── */
    .helpers-ribbon {{
        display: flex;
        gap: 0.6rem;
        flex-wrap: wrap;
        margin: 0.4rem 0 0.8rem 0;
    }}
    .helper-tag {{
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        background: {t["surface"]};
        border: 1px solid {t["card_border"]};
        padding: 0.3rem 0.7rem;
        border-radius: 2rem;
        font-size: 0.88rem;
        font-weight: 500;
        color: {t["text_muted"]};
    }}

    /* ── Layout zones row ───────────────────────────── */
    .zone-row {{
        display: flex;
        gap: 0;
        margin: 0.6rem 0 1.2rem 0;
        border-radius: 0.5rem;
        overflow: hidden;
        border: 1px solid {t["card_border"]};
    }}
    .zone-cell {{
        flex: 1;
        padding: 0.8rem 1rem;
        font-size: 0.95rem;
        line-height: 1.5;
    }}
    .zone-cell-label {{
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        opacity: 0.6;
        margin-bottom: 0.25rem;
    }}
    .zone-cell-title {{
        font-weight: 700;
        margin-bottom: 0.15rem;
    }}
    .zone-nav {{
        background: {t["sidebar_bg"]};
    }}
    .zone-nav, .zone-nav * {{
        color: {t["sidebar_text"]} !important;
    }}
    .zone-wiz {{
        background: {t["bg"]};
        border-left: 1px solid {t["card_border"]};
        border-right: 1px solid {t["card_border"]};
    }}
    .zone-cvs {{
        background: {t["canvas_bg"]};
    }}
    .zone-cvs, .zone-cvs * {{
        color: {t["canvas_text"]} !important;
    }}

    /* ── Journey list ───────────────────────────────── */
    .journey-list {{
        margin: 0.5rem 0;
        padding: 0;
    }}
    .journey-item {{
        display: flex;
        align-items: baseline;
        gap: 0.6rem;
        padding: 0.45rem 0;
        border-bottom: 1px solid {t["divider"]};
        font-size: 1.05rem;
    }}
    .journey-item:last-child {{
        border-bottom: none;
    }}
    .journey-num {{
        flex-shrink: 0;
        width: 26px;
        height: 26px;
        border-radius: 50%;
        background: {t["accent"]};
        color: white !important;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.78rem;
        font-weight: 700;
    }}
    .journey-num.done {{
        background: #10B981;
    }}
    .journey-name {{
        font-weight: 600;
        min-width: 140px;
        color: {t["text"]};
    }}
    .journey-desc {{
        color: {t["text_muted"]};
        font-size: 0.98rem;
    }}

    /* ── Deliverable row ────────────────────────────── */
    .deliv-row {{
        display: flex;
        gap: 1rem;
        margin: 0.5rem 0;
    }}
    .deliv-item {{
        flex: 1;
        background: {t["surface"]};
        border: 1px solid {t["card_border"]};
        border-radius: 0.5rem;
        padding: 0.75rem 1rem;
        font-size: 0.98rem;
        line-height: 1.45;
    }}
    .deliv-item b {{
        display: block;
        margin-bottom: 0.2rem;
    }}

    /* ── CTA ─────────────────────────────────────────── */
    .cta-line {{
        margin-top: 0.8rem;
        padding: 0.7rem 1rem;
        border-left: 3px solid {t["accent"]};
        font-size: 1.05rem;
        color: {t["text"]};
    }}
</style>
"""


def inject_custom_css():
    """Inject the theme CSS based on the current day/night mode."""
    is_dark = st.session_state.get("dark_mode", False)
    palette = DARK if is_dark else LIGHT
    st.markdown(_build_css(palette), unsafe_allow_html=True)


def step_header(step_num: int, title: str, subtitle: str):
    """Render a consistent step header with step badge."""
    st.markdown(
        f'<span class="step-badge">Step {step_num} of 7</span>',
        unsafe_allow_html=True,
    )
    st.header(title)
    st.caption(subtitle)
