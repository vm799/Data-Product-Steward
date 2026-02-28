"""
Theme system — Navy/Teal dual-theme with glassmorphism.
Asset management aesthetic: institutional trust, modern precision.

Light: White base, navy text, teal accent, medium-navy sidebar
Dark:  Deep navy base, light text, bright teal accent, glassmorphism
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
    # Sidebar — readable medium navy, NOT near-black
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
    # Canvas right panel — light teal tint
    "canvas_panel_bg": "#F0FAF9",
    "canvas_panel_border": "#0D9488",
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
    # Sidebar — visible dark navy, not black
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
    # Canvas right panel — darker navy with teal border
    "canvas_panel_bg": "#0D1E33",
    "canvas_panel_border": "rgba(45, 212, 191, 0.30)",
}


def _build_css(t: dict) -> str:
    """Build the full CSS string from a theme palette."""
    return f"""
<style>
    /* ═══════════════════════════════════════════════════════════
       GDP DATA PRODUCT STEWARD — THEME
       Navy + Teal · Glassmorphism · Asset Management Grade
       ═══════════════════════════════════════════════════════════ */

    /* ── App background ────────────────────────────────────────── */
    .stApp {{
        background: {t["bg"]};
        color: {t["text"]};
    }}

    /* ── Main container ────────────────────────────────────────── */
    .main .block-container {{
        padding: 1.5rem 1.5rem 2rem 1.5rem;
        max-width: 100%;
    }}
    [data-testid="stAppViewContainer"] > .main {{
        font-size: 1.08rem;
        line-height: 1.65;
        color: {t["text"]};
    }}

    /* ── Header ────────────────────────────────────────────────── */
    [data-testid="stHeader"] {{
        background: transparent;
    }}

    /* ── Typography ────────────────────────────────────────────── */
    h1 {{
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em;
        color: {t["text"]} !important;
    }}
    h2 {{
        font-size: 1.55rem !important;
        font-weight: 600 !important;
        color: {t["text"]} !important;
    }}
    h3 {{
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        color: {t["text"]} !important;
    }}

    /* ── Markdown text ─────────────────────────────────────────── */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {{
        color: {t["text"]};
    }}
    [data-testid="stMarkdownContainer"] strong {{
        color: {t["text"]};
    }}
    .stCaption, [data-testid="stCaptionContainer"] {{
        color: {t["text_muted"]} !important;
    }}

    /* ── Form labels ───────────────────────────────────────────── */
    .stTextInput label p,
    .stSelectbox label p,
    .stMultiSelect label p,
    .stTextArea label p,
    .stSlider label p,
    .stNumberInput label p,
    .stCheckbox label p {{
        font-size: 1.02rem !important;
        font-weight: 500 !important;
        color: {t["text"]} !important;
    }}

    /* ── Inputs — glassmorphism ─────────────────────────────────── */
    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {{
        background: {t["input_bg"]} !important;
        border: 1px solid {t["input_border"]} !important;
        border-radius: 0.5rem !important;
        color: {t["text"]} !important;
    }}
    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stNumberInput input:focus {{
        border-color: {t["accent"]} !important;
        box-shadow: 0 0 0 2px {t["accent_light"]} !important;
    }}

    /* ── Select boxes ──────────────────────────────────────────── */
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

    /* ── Metric cards — glassmorphism ──────────────────────────── */
    [data-testid="stMetric"] {{
        background: {t["card_bg"]};
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 0.85rem 1rem;
        border-radius: 0.75rem;
        border: 1px solid {t["metric_border"]};
        box-shadow: {t["card_shadow"]};
    }}
    [data-testid="stMetric"] label {{
        color: {t["text_muted"]} !important;
    }}
    [data-testid="stMetric"] [data-testid="stMetricValue"] {{
        color: {t["accent"]} !important;
        font-weight: 700 !important;
    }}

    /* ── Progress bar — teal accent ────────────────────────────── */
    .stProgress > div > div > div {{
        background: {t["gradient"]} !important;
    }}
    .stProgress > div > div {{
        background: {t["accent_light"]} !important;
    }}

    /* ═══════════════════════════════════════════════════════════
       SIDEBAR — readable navy, larger font, high contrast
       ═══════════════════════════════════════════════════════════ */
    section[data-testid="stSidebar"] {{
        background: {t["sidebar_bg"]} !important;
        font-size: 1.05rem;
    }}
    /* Force ALL text in sidebar to be readable */
    section[data-testid="stSidebar"] * {{
        color: {t["sidebar_text"]} !important;
    }}
    /* Headings brighter */
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
    /* Muted text */
    section[data-testid="stSidebar"] .stCaption *,
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {{
        color: {t["sidebar_muted"]} !important;
    }}
    /* Dividers */
    section[data-testid="stSidebar"] hr {{
        border-color: {t["sidebar_divider"]} !important;
    }}
    /* Expander header text */
    section[data-testid="stSidebar"] .streamlit-expanderHeader p {{
        color: {t["sidebar_text"]} !important;
        font-size: 1.05rem !important;
    }}
    /* Toggle label */
    section[data-testid="stSidebar"] .stToggle label span p {{
        color: {t["sidebar_text"]} !important;
        font-size: 1.05rem !important;
    }}
    /* Progress bar in sidebar */
    section[data-testid="stSidebar"] .stProgress > div > div > div {{
        background: {t["gradient"]} !important;
    }}

    /* ── Guide card (sidebar) — visible teal accent ──────────── */
    .guide-card {{
        background: {t["guide_bg"]};
        border-left: 3px solid {t["guide_border"]};
        padding: 0.8rem;
        border-radius: 0 0.4rem 0.4rem 0;
        font-size: 0.95rem;
        line-height: 1.55;
        margin-bottom: 0.5rem;
    }}
    .guide-card, .guide-card * {{
        color: {t["guide_text"]} !important;
    }}

    /* ═══════════════════════════════════════════════════════════
       CANVAS RIGHT PANEL — distinct tinted background
       Targets the last column in the top-level column split
       ═══════════════════════════════════════════════════════════ */
    .canvas-panel {{
        background: {t["canvas_panel_bg"]};
        border-left: 2px solid {t["canvas_panel_border"]};
        border-radius: 0 0.75rem 0.75rem 0;
        padding: 1rem;
        min-height: 400px;
    }}

    /* ── Step badge ────────────────────────────────────────────── */
    .step-badge {{
        display: inline-block;
        background: {t["step_badge_bg"]};
        color: {t["step_badge_text"]};
        padding: 0.2rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
        letter-spacing: 0.02em;
    }}

    /* ── Canvas header — teal gradient ─────────────────────────── */
    .canvas-header {{
        background: {t["gradient"]};
        color: white !important;
        padding: 0.65rem 1rem;
        border-radius: 0.6rem 0.6rem 0 0;
        font-weight: 600;
        font-size: 1.05rem;
        margin-bottom: 0;
    }}
    .canvas-body {{
        background: {t["card_bg"]};
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid {t["card_border"]};
        border-top: none;
        border-radius: 0 0 0.6rem 0.6rem;
        padding: 0.8rem 1rem;
        font-size: 0.95rem;
        color: {t["text"]};
    }}

    /* ── Expander ──────────────────────────────────────────────── */
    .streamlit-expanderHeader {{
        background: {t["surface"]} !important;
        border-radius: 0.5rem !important;
        color: {t["text"]} !important;
    }}

    /* ── Tabs ──────────────────────────────────────────────────── */
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

    /* ── Code blocks ───────────────────────────────────────────── */
    .stCodeBlock {{
        border-radius: 0.5rem !important;
    }}

    /* ── Alerts ────────────────────────────────────────────────── */
    .stAlert {{
        border-radius: 0.5rem !important;
    }}

    /* ── Dividers ──────────────────────────────────────────────── */
    hr {{
        border-color: {t["divider"]} !important;
    }}

    /* ── Download buttons ──────────────────────────────────────── */
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

    /* ── Form submit button ────────────────────────────────────── */
    .stFormSubmitButton button {{
        background: {t["gradient"]} !important;
        color: white !important;
        border: none !important;
        border-radius: 0.5rem !important;
        font-weight: 600 !important;
        padding: 0.5rem 2rem !important;
    }}

    /* ── Regular buttons ───────────────────────────────────────── */
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

    /* ═══════════════════════════════════════════════════════════
       ONBOARDING — Dashboard hero, zone cards, journey steps
       ═══════════════════════════════════════════════════════════ */

    /* ── Dashboard hero banner ────────────────────────────────── */
    .dashboard-hero {{
        background: {t["gradient"]};
        color: white !important;
        padding: 1.5rem 2rem;
        border-radius: 0.75rem;
        margin-bottom: 1rem;
    }}
    .dashboard-hero h1 {{
        color: white !important;
        margin-bottom: 0.3rem;
    }}
    .dashboard-hero p {{
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 1.1rem;
        margin: 0;
    }}

    /* ── Onboarding section heading ──────────────────────────── */
    .onboard-section {{
        margin-bottom: 0.5rem;
    }}
    .onboard-section h3 {{
        margin-bottom: 0.3rem;
    }}
    .onboard-section p {{
        font-size: 1rem;
        line-height: 1.6;
    }}

    /* ── Zone explanation cards (sidebar / wizard / canvas) ───── */
    .zone-card {{
        padding: 1rem;
        border-radius: 0.6rem;
        font-size: 0.92rem;
        line-height: 1.5;
        min-height: 160px;
        border: 1px solid {t["card_border"]};
    }}
    .zone-label {{
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
        opacity: 0.7;
    }}
    .zone-sidebar {{
        background: {t["sidebar_bg"]};
        color: {t["sidebar_text"]} !important;
        border-color: {t["sidebar_bg"]};
    }}
    .zone-sidebar, .zone-sidebar * {{
        color: {t["sidebar_text"]} !important;
    }}
    .zone-wizard {{
        background: {t["surface"]};
    }}
    .zone-canvas {{
        background: {t["canvas_panel_bg"]};
        border-color: {t["canvas_panel_border"]};
    }}

    /* ── 7-step journey cards ────────────────────────────────── */
    .journey-step {{
        display: flex;
        gap: 1rem;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        border-radius: 0.5rem;
        border: 1px solid {t["card_border"]};
        background: {t["surface"]};
    }}
    .journey-step-badge {{
        flex-shrink: 0;
        width: 48px;
        height: 48px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.85rem;
        font-weight: 700;
        line-height: 1;
        text-align: center;
    }}
    .journey-step-badge.step-pending {{
        background: {t["step_badge_bg"]};
        color: {t["step_badge_text"]};
    }}
    .journey-step-badge.step-done {{
        background: rgba(16, 185, 129, 0.12);
        color: #10B981;
        font-size: 1.2rem;
    }}
    .journey-step-body {{
        flex: 1;
    }}
    .journey-step-title {{
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 0.2rem;
        color: {t["text"]};
    }}
    .journey-step-what,
    .journey-step-why {{
        font-size: 0.92rem;
        line-height: 1.5;
        margin-bottom: 0.15rem;
        color: {t["text"]};
    }}
    .journey-step-produces {{
        font-size: 0.82rem;
        color: {t["accent"]};
        font-weight: 500;
        margin-top: 0.2rem;
    }}

    /* ── Deliverable cards ────────────────────────────────────── */
    .deliverable-card {{
        background: {t["surface"]};
        border: 1px solid {t["card_border"]};
        border-radius: 0.6rem;
        padding: 1rem;
        font-size: 0.92rem;
        line-height: 1.5;
        min-height: 120px;
    }}

    /* ── Call-to-action box ───────────────────────────────────── */
    .cta-box {{
        background: {t["accent_light"]};
        border: 2px solid {t["accent"]};
        border-radius: 0.6rem;
        padding: 1rem 1.5rem;
        font-size: 1.05rem;
        text-align: center;
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
