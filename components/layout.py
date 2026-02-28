"""
Theme — dark glassmorphism + retro hacker aesthetic.

Deep gradient background, frosted-glass panels, Share Tech Mono font,
pulsing teal canvas glow. No flat block colours.
"""

import streamlit as st


def _css() -> str:
    return """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

    /* ═══════════════════════════════════════════════════
       GLOBAL — font, background, reset
       ═══════════════════════════════════════════════════ */
    .stApp, .stApp * {
        font-family: 'Share Tech Mono', monospace !important;
    }
    .stApp {
        background: linear-gradient(160deg, #06080D 0%, #0B1220 50%, #091018 100%) !important;
        color: #E8ECF1;
    }

    /* ── Kill top whitespace ────────────────────────── */
    .main .block-container {
        padding: 0.6rem 1.5rem 2rem 1.5rem !important;
        max-width: 100%;
    }
    [data-testid="stHeader"] {
        background: transparent !important;
        height: 0 !important;
        min-height: 0 !important;
        overflow: hidden;
    }

    /* ═══════════════════════════════════════════════════
       TYPOGRAPHY — retro terminal
       ═══════════════════════════════════════════════════ */
    [data-testid="stAppViewContainer"] > .main {
        font-size: 1.12rem;
        line-height: 1.7;
        color: #E8ECF1;
    }
    h1 {
        font-size: 1.9rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #2DD4BF !important;
    }
    h2 {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: #2DD4BF !important;
    }
    h3 {
        font-size: 1.25rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        color: #2DD4BF !important;
    }
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        color: #E8ECF1;
        font-size: 1.08rem;
    }
    [data-testid="stMarkdownContainer"] strong {
        color: #E8ECF1;
    }
    .stCaption, [data-testid="stCaptionContainer"] {
        color: #8B95A5 !important;
        font-size: 0.92rem !important;
    }

    /* ── Form labels ────────────────────────────────── */
    .stTextInput label p,
    .stSelectbox label p,
    .stMultiSelect label p,
    .stTextArea label p,
    .stSlider label p,
    .stNumberInput label p,
    .stCheckbox label p {
        font-size: 1.02rem !important;
        font-weight: 500 !important;
        color: #E8ECF1 !important;
    }

    /* ── Glass inputs ───────────────────────────────── */
    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 0.5rem !important;
        color: #E8ECF1 !important;
        font-size: 1.02rem !important;
        backdrop-filter: blur(8px);
    }
    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stNumberInput input:focus {
        border-color: #2DD4BF !important;
        box-shadow: 0 0 0 2px rgba(45,212,191,0.25) !important;
    }
    .stSelectbox [data-baseweb="select"],
    .stMultiSelect [data-baseweb="select"] {
        background: rgba(255,255,255,0.04) !important;
        border-color: rgba(255,255,255,0.10) !important;
    }
    .stSelectbox [data-baseweb="select"] > div,
    .stMultiSelect [data-baseweb="select"] > div {
        background: rgba(255,255,255,0.04) !important;
        color: #E8ECF1 !important;
    }

    /* ── Glass metrics ──────────────────────────────── */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.04);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        padding: 0.85rem 1rem;
        border-radius: 0.75rem;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 4px 24px rgba(0,0,0,0.15);
    }
    [data-testid="stMetric"] label {
        color: #8B95A5 !important;
        font-size: 0.85rem !important;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #2DD4BF !important;
        font-weight: 700 !important;
    }

    /* ── Progress bar ───────────────────────────────── */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #2DD4BF 0%, #22D3EE 100%) !important;
    }
    .stProgress > div > div {
        background: rgba(45,212,191,0.08) !important;
    }

    /* ═══════════════════════════════════════════════════
       CENTER WIZARD PANEL — frosted white glass
       ═══════════════════════════════════════════════════ */
    .wizard-panel {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 0.75rem;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.20);
    }

    /* ═══════════════════════════════════════════════════
       SIDEBAR — frosted dark glass
       ═══════════════════════════════════════════════════ */
    section[data-testid="stSidebar"] {
        background: rgba(8,12,22,0.85) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255,255,255,0.06) !important;
        font-size: 1.02rem;
    }
    section[data-testid="stSidebar"] * {
        color: #8B95A5 !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #E8ECF1 !important;
    }
    section[data-testid="stSidebar"] h1 {
        font-size: 1.35rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.04em;
    }
    section[data-testid="stSidebar"] h3 {
        font-size: 1.1rem !important;
        font-weight: 500 !important;
    }
    section[data-testid="stSidebar"] .stCaption *,
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {
        color: #5A6478 !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.08) !important;
    }
    section[data-testid="stSidebar"] .streamlit-expanderHeader p,
    section[data-testid="stSidebar"] .stToggle label span p {
        color: #8B95A5 !important;
        font-size: 1.02rem !important;
    }
    section[data-testid="stSidebar"] .stProgress > div > div > div {
        background: linear-gradient(135deg, #2DD4BF 0%, #22D3EE 100%) !important;
    }

    /* ── "Dashboard" home link — retro ──────────────── */
    [data-testid="stSidebarNav"] li:first-child span {
        font-size: 0 !important;
    }
    [data-testid="stSidebarNav"] li:first-child span::after {
        content: "> DASHBOARD_";
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 1.05rem;
        letter-spacing: 0.08em;
        color: #2DD4BF !important;
        text-shadow: 0 0 8px rgba(45,212,191,0.4);
    }
    [data-testid="stSidebarNav"] li:first-child:hover span::after {
        text-shadow: 0 0 14px rgba(45,212,191,0.7);
        color: #5EEAD4 !important;
    }

    /* ── Guide card ─────────────────────────────────── */
    .guide-card {
        background: rgba(45,212,191,0.06);
        border-left: 2px solid #2DD4BF;
        padding: 0.75rem 0.85rem;
        border-radius: 0 0.4rem 0.4rem 0;
        font-size: 0.95rem;
        line-height: 1.55;
        margin-bottom: 0.5rem;
    }
    .guide-card, .guide-card * {
        color: #8B95A5 !important;
    }

    /* ═══════════════════════════════════════════════════
       CANVAS — glass + pulsing teal glow
       ═══════════════════════════════════════════════════ */
    @keyframes canvasPulse {
        0%   { box-shadow: 0 0 20px rgba(45,212,191,0.06), 0 0 40px rgba(45,212,191,0.03), inset 0 1px 0 rgba(45,212,191,0.08); border-color: rgba(45,212,191,0.15); }
        50%  { box-shadow: 0 0 35px rgba(45,212,191,0.18), 0 0 70px rgba(45,212,191,0.08), inset 0 1px 0 rgba(45,212,191,0.15); border-color: rgba(45,212,191,0.35); }
        100% { box-shadow: 0 0 20px rgba(45,212,191,0.06), 0 0 40px rgba(45,212,191,0.03), inset 0 1px 0 rgba(45,212,191,0.08); border-color: rgba(45,212,191,0.15); }
    }
    .canvas-panel {
        background: rgba(45,212,191,0.03);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(45,212,191,0.15);
        border-radius: 0.75rem;
        padding: 1.25rem;
        min-height: 480px;
        animation: canvasPulse 3s ease-in-out infinite;
    }
    .canvas-panel, .canvas-panel p, .canvas-panel li,
    .canvas-panel span, .canvas-panel strong, .canvas-panel b {
        color: #E8ECF1 !important;
    }
    .canvas-panel .stCaption *,
    .canvas-panel [data-testid="stCaptionContainer"] * {
        color: #8B95A5 !important;
    }
    .canvas-panel hr {
        border-color: rgba(255,255,255,0.08) !important;
    }
    .canvas-panel [data-testid="stMetric"] {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: none;
    }
    .canvas-panel [data-testid="stMetric"] label {
        color: #8B95A5 !important;
    }
    .canvas-panel [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #2DD4BF !important;
    }
    .canvas-panel .stDownloadButton button {
        background: rgba(255,255,255,0.06) !important;
        color: #E8ECF1 !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
    }
    .canvas-panel .stDownloadButton button:hover {
        background: rgba(255,255,255,0.10) !important;
    }
    .canvas-panel .streamlit-expanderHeader {
        background: rgba(255,255,255,0.04) !important;
        color: #E8ECF1 !important;
    }
    .canvas-panel .streamlit-expanderHeader p {
        color: #E8ECF1 !important;
    }

    /* ── LIVE CANVAS label — pulsing glow ───────────── */
    @keyframes labelPulse {
        0%   { text-shadow: 0 0 8px rgba(45,212,191,0.5), 0 0 16px rgba(45,212,191,0.25); }
        50%  { text-shadow: 0 0 14px rgba(45,212,191,0.8), 0 0 28px rgba(45,212,191,0.4); }
        100% { text-shadow: 0 0 8px rgba(45,212,191,0.5), 0 0 16px rgba(45,212,191,0.25); }
    }
    .canvas-label {
        font-size: 0.9rem;
        font-weight: 700;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #2DD4BF !important;
        margin-bottom: 0.15rem;
        animation: labelPulse 2s ease-in-out infinite;
    }
    .canvas-heading {
        font-size: 1.15rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        color: #E8ECF1 !important;
        margin-bottom: 0.2rem;
    }
    .canvas-explain {
        color: #8B95A5 !important;
        font-size: 0.92rem;
        line-height: 1.55;
        margin-bottom: 0.8rem;
    }
    .canvas-body {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 0.5rem;
        padding: 0.8rem 1rem;
        font-size: 0.98rem;
        color: #E8ECF1;
    }

    /* ── Step badge ──────────────────────────────────── */
    .step-badge {
        display: inline-block;
        background: rgba(45,212,191,0.08);
        color: #2DD4BF;
        padding: 0.2rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
        letter-spacing: 0.02em;
    }

    /* ── Expander / Tabs / Alerts ────────────────────── */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.04) !important;
        border-radius: 0.5rem !important;
        color: #E8ECF1 !important;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 0.5rem; }
    .stTabs [data-baseweb="tab"] {
        color: #8B95A5 !important;
        border-radius: 0.5rem 0.5rem 0 0;
    }
    .stTabs [aria-selected="true"] {
        color: #2DD4BF !important;
        border-bottom-color: #2DD4BF !important;
    }
    .stCodeBlock { border-radius: 0.5rem !important; }
    .stAlert { border-radius: 0.5rem !important; }
    hr { border-color: rgba(255,255,255,0.08) !important; }

    /* ── Buttons ─────────────────────────────────────── */
    .stDownloadButton button {
        background: linear-gradient(135deg, #2DD4BF 0%, #22D3EE 100%) !important;
        color: #06080D !important;
        border: none !important;
        border-radius: 0.5rem !important;
        font-weight: 600 !important;
    }
    .stDownloadButton button:hover { opacity: 0.9; }
    .stFormSubmitButton button {
        background: linear-gradient(135deg, #2DD4BF 0%, #22D3EE 100%) !important;
        color: #06080D !important;
        border: none !important;
        border-radius: 0.5rem !important;
        font-weight: 600 !important;
        padding: 0.5rem 2rem !important;
    }
    .stButton > button {
        border: 1px solid rgba(255,255,255,0.12) !important;
        color: #2DD4BF !important;
        border-radius: 0.5rem !important;
        background: transparent !important;
    }
    .stButton > button:hover {
        background: rgba(45,212,191,0.08) !important;
        border-color: #2DD4BF !important;
    }

    /* ═══════════════════════════════════════════════════
       HOME PAGE — journey + deliverables
       ═══════════════════════════════════════════════════ */
    .journey-list { margin: 0.4rem 0; }
    .journey-item {
        display: flex;
        align-items: baseline;
        gap: 0.6rem;
        padding: 0.4rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        font-size: 1rem;
    }
    .journey-item:last-child { border-bottom: none; }
    .journey-num {
        flex-shrink: 0;
        width: 24px; height: 24px;
        border-radius: 50%;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        color: #8B95A5 !important;
        display: inline-flex;
        align-items: center; justify-content: center;
        font-size: 0.72rem; font-weight: 600;
    }
    .journey-num.done {
        background: rgba(45,212,191,0.10);
        border-color: #2DD4BF;
        color: #2DD4BF !important;
    }
    .journey-name {
        font-weight: 600;
        min-width: 130px;
        color: #E8ECF1;
    }
    .journey-desc {
        color: #8B95A5;
        font-size: 0.92rem;
    }
    .deliv-row {
        display: flex; gap: 0.75rem; margin: 0.4rem 0;
    }
    .deliv-item {
        flex: 1;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 0.5rem;
        padding: 0.7rem 0.85rem;
        font-size: 0.9rem; line-height: 1.45;
        backdrop-filter: blur(8px);
        color: #8B95A5;
    }
    .deliv-item b { display: block; margin-bottom: 0.15rem; color: #E8ECF1; }
    .cta-line {
        margin-top: 0.6rem;
        padding: 0.65rem 1rem;
        border-left: 2px solid #2DD4BF;
        font-size: 1rem;
        color: #8B95A5;
    }
    .cta-line b { color: #E8ECF1; }

    /* ── Sidebar label ──────────────────────────────── */
    .sidebar-label {
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #5A6478 !important;
        margin-bottom: 0.2rem;
    }
</style>
"""


def inject_custom_css():
    """Inject retro hacker glassmorphism theme."""
    st.markdown(_css(), unsafe_allow_html=True)


def step_header(step_num: int, title: str, subtitle: str):
    """Render a consistent step header with step badge."""
    st.markdown(
        f'<span class="step-badge">Step {step_num} of 7</span>',
        unsafe_allow_html=True,
    )
    st.header(title)
    st.caption(subtitle)
