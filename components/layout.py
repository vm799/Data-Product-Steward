"""
Theme — dark glassmorphism.

Deep gradient background, frosted-glass panels, luminous teal accents.
No flat block colours anywhere. Depth through blur, translucency, and glow.
"""

import streamlit as st

# ── Palette ─────────────────────────────────────────────────────────────
# Single dark palette. Light toggle adjusts intensity, not a full swap.
P = {
    # Background gradient endpoints
    "bg_from": "#06080D",
    "bg_to": "#0B1220",
    "bg_accent": "#091018",
    # Glass surfaces
    "glass": "rgba(255,255,255,0.04)",
    "glass_hover": "rgba(255,255,255,0.07)",
    "glass_border": "rgba(255,255,255,0.08)",
    "glass_strong": "rgba(255,255,255,0.06)",
    "glass_strong_border": "rgba(255,255,255,0.12)",
    # Text
    "text": "#E8ECF1",
    "text_secondary": "#8B95A5",
    "text_dim": "#5A6478",
    # Accent — teal/cyan
    "accent": "#2DD4BF",
    "accent_secondary": "#22D3EE",
    "accent_glow": "rgba(45,212,191,0.15)",
    "accent_glow_strong": "rgba(45,212,191,0.25)",
    "accent_dim": "rgba(45,212,191,0.08)",
    "accent_text": "#2DD4BF",
    # Gradient
    "gradient": "linear-gradient(135deg, #2DD4BF 0%, #22D3EE 100%)",
    "gradient_subtle": "linear-gradient(135deg, rgba(45,212,191,0.12) 0%, rgba(34,211,238,0.06) 100%)",
    # Sidebar
    "sidebar_bg": "rgba(8,12,22,0.85)",
    "sidebar_border": "rgba(255,255,255,0.06)",
    # Canvas
    "canvas_glass": "rgba(45,212,191,0.04)",
    "canvas_border": "rgba(45,212,191,0.15)",
    "canvas_glow": "0 0 30px rgba(45,212,191,0.08), inset 0 1px 0 rgba(45,212,191,0.10)",
    # Status
    "success": "#10B981",
    "warn": "#F59E0B",
    "error": "#EF4444",
    # Input
    "input_bg": "rgba(255,255,255,0.04)",
    "input_border": "rgba(255,255,255,0.10)",
    "input_focus": "rgba(45,212,191,0.30)",
}


def _css() -> str:
    t = P
    return f"""
<style>
    /* ═══════════════════════════════════════════════════
       DATA PRODUCT BUILDER — GLASSMORPHISM
       ═══════════════════════════════════════════════════ */

    /* ── Dark gradient background ───────────────────── */
    .stApp {{
        background: linear-gradient(160deg, {t["bg_from"]} 0%, {t["bg_to"]} 50%, {t["bg_accent"]} 100%) !important;
        color: {t["text"]};
    }}

    /* ── Kill whitespace, hide default header ───────── */
    .main .block-container {{
        padding: 0.6rem 1.5rem 2rem 1.5rem !important;
        max-width: 100%;
    }}
    [data-testid="stHeader"] {{
        background: transparent !important;
        height: 0 !important;
        min-height: 0 !important;
        overflow: hidden;
    }}

    /* ── Rename "streamlit_app" → "Dashboard" ───────── */
    [data-testid="stSidebarNav"] li:first-child span {{
        font-size: 0 !important;
    }}
    [data-testid="stSidebarNav"] li:first-child span::after {{
        content: "Dashboard";
        font-size: 1.05rem;
    }}

    /* ── Typography ─────────────────────────────────── */
    [data-testid="stAppViewContainer"] > .main {{
        font-size: 1.15rem;
        line-height: 1.7;
        color: {t["text"]};
    }}
    h1 {{
        font-size: 2rem !important;
        font-weight: 600 !important;
        letter-spacing: -0.03em;
        color: {t["text"]} !important;
    }}
    h2 {{
        font-size: 1.6rem !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em;
        color: {t["text"]} !important;
    }}
    h3 {{
        font-size: 1.3rem !important;
        font-weight: 500 !important;
        color: {t["text"]} !important;
    }}
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {{
        color: {t["text"]};
        font-size: 1.1rem;
    }}
    [data-testid="stMarkdownContainer"] strong {{
        color: {t["text"]};
    }}
    .stCaption, [data-testid="stCaptionContainer"] {{
        color: {t["text_secondary"]} !important;
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
        font-size: 1.05rem !important;
        font-weight: 500 !important;
        color: {t["text"]} !important;
    }}

    /* ── Glass inputs ───────────────────────────────── */
    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {{
        background: {t["input_bg"]} !important;
        border: 1px solid {t["input_border"]} !important;
        border-radius: 0.5rem !important;
        color: {t["text"]} !important;
        font-size: 1.05rem !important;
        backdrop-filter: blur(8px);
    }}
    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stNumberInput input:focus {{
        border-color: {t["accent"]} !important;
        box-shadow: 0 0 0 2px {t["input_focus"]} !important;
    }}
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

    /* ── Glass metric cards ─────────────────────────── */
    [data-testid="stMetric"] {{
        background: {t["glass"]};
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        padding: 0.85rem 1rem;
        border-radius: 0.75rem;
        border: 1px solid {t["glass_border"]};
        box-shadow: 0 4px 24px rgba(0,0,0,0.15);
    }}
    [data-testid="stMetric"] label {{
        color: {t["text_secondary"]} !important;
        font-size: 0.88rem !important;
    }}
    [data-testid="stMetric"] [data-testid="stMetricValue"] {{
        color: {t["accent_text"]} !important;
        font-weight: 700 !important;
    }}

    /* ── Progress bar ───────────────────────────────── */
    .stProgress > div > div > div {{
        background: {t["gradient"]} !important;
    }}
    .stProgress > div > div {{
        background: {t["accent_dim"]} !important;
    }}

    /* ═══════════════════════════════════════════════════
       SIDEBAR — frosted glass
       ═══════════════════════════════════════════════════ */
    section[data-testid="stSidebar"] {{
        background: {t["sidebar_bg"]} !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-right: 1px solid {t["sidebar_border"]} !important;
        font-size: 1.05rem;
    }}
    section[data-testid="stSidebar"] * {{
        color: {t["text_secondary"]} !important;
    }}
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: {t["text"]} !important;
    }}
    section[data-testid="stSidebar"] h1 {{
        font-size: 1.4rem !important;
        font-weight: 600 !important;
    }}
    section[data-testid="stSidebar"] h3 {{
        font-size: 1.15rem !important;
        font-weight: 500 !important;
    }}
    section[data-testid="stSidebar"] .stCaption *,
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {{
        color: {t["text_dim"]} !important;
    }}
    section[data-testid="stSidebar"] hr {{
        border-color: {t["glass_border"]} !important;
    }}
    section[data-testid="stSidebar"] .streamlit-expanderHeader p,
    section[data-testid="stSidebar"] .stToggle label span p {{
        color: {t["text_secondary"]} !important;
        font-size: 1.05rem !important;
    }}
    section[data-testid="stSidebar"] .stProgress > div > div > div {{
        background: {t["gradient"]} !important;
    }}

    /* ── Guide card ─────────────────────────────────── */
    .guide-card {{
        background: {t["accent_dim"]};
        border-left: 2px solid {t["accent"]};
        padding: 0.75rem 0.85rem;
        border-radius: 0 0.4rem 0.4rem 0;
        font-size: 0.98rem;
        line-height: 1.55;
        margin-bottom: 0.5rem;
    }}
    .guide-card, .guide-card * {{
        color: {t["text_secondary"]} !important;
    }}

    /* ═══════════════════════════════════════════════════
       CANVAS — glass with teal glow, NOT solid block
       ═══════════════════════════════════════════════════ */
    .canvas-panel {{
        background: {t["canvas_glass"]};
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid {t["canvas_border"]};
        border-radius: 0.75rem;
        padding: 1.25rem;
        min-height: 480px;
        box-shadow: {t["canvas_glow"]};
    }}
    .canvas-panel, .canvas-panel p, .canvas-panel li,
    .canvas-panel span, .canvas-panel strong, .canvas-panel b {{
        color: {t["text"]} !important;
    }}
    .canvas-panel .stCaption *,
    .canvas-panel [data-testid="stCaptionContainer"] * {{
        color: {t["text_secondary"]} !important;
    }}
    .canvas-panel hr {{
        border-color: {t["glass_border"]} !important;
    }}
    .canvas-panel [data-testid="stMetric"] {{
        background: {t["glass"]};
        border: 1px solid {t["glass_border"]};
        box-shadow: none;
    }}
    .canvas-panel [data-testid="stMetric"] label {{
        color: {t["text_secondary"]} !important;
    }}
    .canvas-panel [data-testid="stMetric"] [data-testid="stMetricValue"] {{
        color: {t["accent_text"]} !important;
    }}
    .canvas-panel .stDownloadButton button {{
        background: {t["glass_strong"]} !important;
        color: {t["text"]} !important;
        border: 1px solid {t["glass_strong_border"]} !important;
    }}
    .canvas-panel .stDownloadButton button:hover {{
        background: {t["glass_hover"]} !important;
    }}
    .canvas-panel .streamlit-expanderHeader {{
        background: {t["glass"]} !important;
        color: {t["text"]} !important;
    }}
    .canvas-panel .streamlit-expanderHeader p {{
        color: {t["text"]} !important;
    }}

    /* ── Canvas typography ───────────────────────────── */
    .canvas-title {{
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: {t["accent_text"]} !important;
        margin-bottom: 0.15rem;
    }}
    .canvas-heading {{
        font-size: 1.2rem;
        font-weight: 600;
        color: {t["text"]} !important;
        margin-bottom: 0.2rem;
    }}
    .canvas-explain {{
        color: {t["text_secondary"]} !important;
        font-size: 0.95rem;
        line-height: 1.55;
        margin-bottom: 0.8rem;
    }}
    .canvas-body {{
        background: {t["glass"]};
        border: 1px solid {t["glass_border"]};
        border-radius: 0.5rem;
        padding: 0.8rem 1rem;
        font-size: 1rem;
        color: {t["text"]};
    }}

    /* ── Step badge ──────────────────────────────────── */
    .step-badge {{
        display: inline-block;
        background: {t["accent_dim"]};
        color: {t["accent_text"]};
        padding: 0.2rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.88rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
        letter-spacing: 0.02em;
    }}

    /* ── Expander ────────────────────────────────────── */
    .streamlit-expanderHeader {{
        background: {t["glass"]} !important;
        border-radius: 0.5rem !important;
        color: {t["text"]} !important;
    }}

    /* ── Tabs ────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: {t["text_secondary"]} !important;
        border-radius: 0.5rem 0.5rem 0 0;
    }}
    .stTabs [aria-selected="true"] {{
        color: {t["accent"]} !important;
        border-bottom-color: {t["accent"]} !important;
    }}

    /* ── Code / Alerts ──────────────────────────────── */
    .stCodeBlock {{
        border-radius: 0.5rem !important;
    }}
    .stAlert {{
        border-radius: 0.5rem !important;
    }}

    /* ── Dividers ────────────────────────────────────── */
    hr {{
        border-color: {t["glass_border"]} !important;
    }}

    /* ── Buttons ─────────────────────────────────────── */
    .stDownloadButton button {{
        background: {t["gradient"]} !important;
        color: #06080D !important;
        border: none !important;
        border-radius: 0.5rem !important;
        font-weight: 600 !important;
    }}
    .stDownloadButton button:hover {{
        opacity: 0.9;
    }}
    .stFormSubmitButton button {{
        background: {t["gradient"]} !important;
        color: #06080D !important;
        border: none !important;
        border-radius: 0.5rem !important;
        font-weight: 600 !important;
        padding: 0.5rem 2rem !important;
    }}
    .stButton > button {{
        border: 1px solid {t["glass_strong_border"]} !important;
        color: {t["accent_text"]} !important;
        border-radius: 0.5rem !important;
        background: transparent !important;
    }}
    .stButton > button:hover {{
        background: {t["accent_dim"]} !important;
        border-color: {t["accent"]} !important;
    }}

    /* ═══════════════════════════════════════════════════
       HOME PAGE — editorial components
       ═══════════════════════════════════════════════════ */

    /* ── Helpers ribbon ─────────────────────────────── */
    .helpers-ribbon {{
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin: 0.3rem 0 0.6rem 0;
    }}
    .helper-tag {{
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        background: {t["glass"]};
        border: 1px solid {t["glass_border"]};
        padding: 0.25rem 0.65rem;
        border-radius: 2rem;
        font-size: 0.82rem;
        font-weight: 500;
        color: {t["text_secondary"]};
        backdrop-filter: blur(8px);
    }}

    /* ── Layout zone row ────────────────────────────── */
    .zone-row {{
        display: flex;
        gap: 0;
        margin: 0.5rem 0 1rem 0;
        border-radius: 0.5rem;
        overflow: hidden;
        border: 1px solid {t["glass_border"]};
    }}
    .zone-cell {{
        flex: 1;
        padding: 0.7rem 0.85rem;
        font-size: 0.9rem;
        line-height: 1.5;
    }}
    .zone-cell-label {{
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        opacity: 0.5;
        margin-bottom: 0.2rem;
    }}
    .zone-cell-title {{
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 0.1rem;
    }}
    .zone-nav {{
        background: {t["sidebar_bg"]};
        backdrop-filter: blur(12px);
    }}
    .zone-nav, .zone-nav * {{
        color: {t["text_secondary"]} !important;
    }}
    .zone-wiz {{
        background: {t["glass"]};
        border-left: 1px solid {t["glass_border"]};
        border-right: 1px solid {t["glass_border"]};
    }}
    .zone-cvs {{
        background: {t["canvas_glass"]};
        border-left: 1px solid {t["canvas_border"]};
    }}
    .zone-cvs, .zone-cvs * {{
        color: {t["text"]} !important;
    }}

    /* ── Journey list ───────────────────────────────── */
    .journey-list {{
        margin: 0.4rem 0;
    }}
    .journey-item {{
        display: flex;
        align-items: baseline;
        gap: 0.6rem;
        padding: 0.4rem 0;
        border-bottom: 1px solid {t["glass_border"]};
        font-size: 1.02rem;
    }}
    .journey-item:last-child {{
        border-bottom: none;
    }}
    .journey-num {{
        flex-shrink: 0;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: {t["glass_strong"]};
        border: 1px solid {t["glass_strong_border"]};
        color: {t["text_secondary"]} !important;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.72rem;
        font-weight: 600;
    }}
    .journey-num.done {{
        background: {t["accent_dim"]};
        border-color: {t["accent"]};
        color: {t["accent_text"]} !important;
    }}
    .journey-name {{
        font-weight: 600;
        min-width: 130px;
        color: {t["text"]};
    }}
    .journey-desc {{
        color: {t["text_secondary"]};
        font-size: 0.95rem;
    }}

    /* ── Deliverables row ───────────────────────────── */
    .deliv-row {{
        display: flex;
        gap: 0.75rem;
        margin: 0.4rem 0;
    }}
    .deliv-item {{
        flex: 1;
        background: {t["glass"]};
        border: 1px solid {t["glass_border"]};
        border-radius: 0.5rem;
        padding: 0.7rem 0.85rem;
        font-size: 0.92rem;
        line-height: 1.45;
        backdrop-filter: blur(8px);
    }}
    .deliv-item b {{
        display: block;
        margin-bottom: 0.15rem;
        color: {t["text"]};
    }}
    .deliv-item {{
        color: {t["text_secondary"]};
    }}

    /* ── CTA ─────────────────────────────────────────── */
    .cta-line {{
        margin-top: 0.6rem;
        padding: 0.65rem 1rem;
        border-left: 2px solid {t["accent"]};
        font-size: 1.02rem;
        color: {t["text_secondary"]};
    }}
    .cta-line b {{
        color: {t["text"]};
    }}
</style>
"""


def inject_custom_css():
    """Inject glassmorphism theme CSS."""
    st.markdown(_css(), unsafe_allow_html=True)


def step_header(step_num: int, title: str, subtitle: str):
    """Render a consistent step header with step badge."""
    st.markdown(
        f'<span class="step-badge">Step {step_num} of 7</span>',
        unsafe_allow_html=True,
    )
    st.header(title)
    st.caption(subtitle)
