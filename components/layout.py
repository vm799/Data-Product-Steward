"""
Theme — dark glassmorphism + retro hacker.
Share Tech Mono, pulsing teal canvas, frosted panels.
Multi-page onboarding: landing, sidebar guide, canvas guide, dashboard.
"""

import streamlit as st


def _css() -> str:
    return """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

    /* ═══════════════════════════════════════════════════
       GLOBAL
       ═══════════════════════════════════════════════════ */
    .stApp {
        background: linear-gradient(160deg, #06080D 0%, #0B1220 50%, #091018 100%) !important;
        color: #E8ECF1;
        font-family: 'Share Tech Mono', monospace !important;
    }
    /* Apply font but NOT to emoji characters */
    .stApp p, .stApp span, .stApp label, .stApp input,
    .stApp textarea, .stApp select, .stApp button,
    .stApp h1, .stApp h2, .stApp h3, .stApp h4,
    .stApp li, .stApp td, .stApp th, .stApp a,
    .stApp div, .stApp code {
        font-family: 'Share Tech Mono', monospace !important;
    }

    /* ── Kill top whitespace ────────────────────────── */
    .main .block-container {
        padding: 0.6rem 1.8rem 2rem 1.8rem !important;
        max-width: 100%;
    }
    [data-testid="stHeader"] {
        background: transparent !important;
        height: 0 !important;
        min-height: 0 !important;
        overflow: hidden;
    }

    /* ═══════════════════════════════════════════════════
       TYPOGRAPHY — clean, no overlap
       ═══════════════════════════════════════════════════ */
    [data-testid="stAppViewContainer"] > .main {
        font-size: 1.15rem;
        line-height: 1.75;
        color: #E8ECF1;
    }
    h1 {
        font-size: 2rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: #2DD4BF !important;
        line-height: 1.3 !important;
        margin-bottom: 0.3rem !important;
    }
    h2 {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em;
        color: #2DD4BF !important;
        line-height: 1.35 !important;
        margin-bottom: 0.25rem !important;
    }
    h3 {
        font-size: 1.2rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.01em;
        color: #2DD4BF !important;
        line-height: 1.4 !important;
        margin-bottom: 0.2rem !important;
    }
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        color: #E8ECF1;
        font-size: 1.1rem;
        line-height: 1.7;
    }
    [data-testid="stMarkdownContainer"] strong { color: #E8ECF1; }
    .stCaption, [data-testid="stCaptionContainer"] {
        color: #8B95A5 !important;
        font-size: 0.95rem !important;
        line-height: 1.5 !important;
    }

    /* ── Form labels ────────────────────────────────── */
    .stTextInput label p, .stSelectbox label p,
    .stMultiSelect label p, .stTextArea label p,
    .stSlider label p, .stNumberInput label p,
    .stCheckbox label p {
        font-size: 1.05rem !important;
        font-weight: 500 !important;
        color: #E8ECF1 !important;
        line-height: 1.5 !important;
    }

    /* ── Glass inputs ───────────────────────────────── */
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 0.5rem !important;
        color: #E8ECF1 !important;
        font-size: 1.05rem !important;
        backdrop-filter: blur(8px);
    }
    .stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {
        border-color: #2DD4BF !important;
        box-shadow: 0 0 0 2px rgba(45,212,191,0.25) !important;
    }
    .stSelectbox [data-baseweb="select"], .stMultiSelect [data-baseweb="select"] {
        background: rgba(255,255,255,0.04) !important;
        border-color: rgba(255,255,255,0.10) !important;
    }
    .stSelectbox [data-baseweb="select"] > div, .stMultiSelect [data-baseweb="select"] > div {
        background: rgba(255,255,255,0.04) !important;
        color: #E8ECF1 !important;
    }

    /* ── Metrics ────────────────────────────────────── */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.04);
        backdrop-filter: blur(16px);
        padding: 0.85rem 1rem;
        border-radius: 0.75rem;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 4px 24px rgba(0,0,0,0.15);
    }
    [data-testid="stMetric"] label {
        color: #8B95A5 !important;
        font-size: 0.88rem !important;
        line-height: 1.3 !important;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #2DD4BF !important;
        font-weight: 700 !important;
        font-size: 1.3rem !important;
        line-height: 1.3 !important;
    }

    /* ── Progress bar ───────────────────────────────── */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #2DD4BF 0%, #22D3EE 100%) !important;
    }
    .stProgress > div > div {
        background: rgba(45,212,191,0.08) !important;
    }

    /* ═══════════════════════════════════════════════════
       WIZARD PANEL — frosted glass
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
       SIDEBAR
       ═══════════════════════════════════════════════════ */
    section[data-testid="stSidebar"] {
        background: rgba(8,12,22,0.85) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255,255,255,0.06) !important;
        font-size: 1.05rem;
    }
    section[data-testid="stSidebar"] * { color: #8B95A5 !important; }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 { color: #E8ECF1 !important; }
    section[data-testid="stSidebar"] h1 {
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.03em;
        line-height: 1.3 !important;
    }
    section[data-testid="stSidebar"] h3 {
        font-size: 1.08rem !important;
        font-weight: 500 !important;
        line-height: 1.3 !important;
    }
    section[data-testid="stSidebar"] .stCaption *,
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {
        color: #5A6478 !important;
    }
    section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.08) !important; }
    section[data-testid="stSidebar"] .streamlit-expanderHeader p,
    section[data-testid="stSidebar"] .stToggle label span p {
        color: #8B95A5 !important;
        font-size: 1.02rem !important;
    }
    section[data-testid="stSidebar"] .stProgress > div > div > div {
        background: linear-gradient(135deg, #2DD4BF 0%, #22D3EE 100%) !important;
    }

    /* ── Dashboard link ─────────────────────────────── */
    [data-testid="stSidebarNav"] li:first-child span { font-size: 0 !important; }
    [data-testid="stSidebarNav"] li:first-child span::after {
        content: "> DASHBOARD_";
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 1.05rem;
        letter-spacing: 0.06em;
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
        font-size: 0.98rem;
        line-height: 1.6;
        margin-bottom: 0.5rem;
    }
    .guide-card, .guide-card * { color: #8B95A5 !important; }

    /* ═══════════════════════════════════════════════════
       CANVAS — glass + pulsing teal glow
       ═══════════════════════════════════════════════════ */
    @keyframes canvasPulse {
        0%   { box-shadow: 0 0 20px rgba(45,212,191,0.06), 0 0 40px rgba(45,212,191,0.03); border-color: rgba(45,212,191,0.15); }
        50%  { box-shadow: 0 0 35px rgba(45,212,191,0.18), 0 0 70px rgba(45,212,191,0.08); border-color: rgba(45,212,191,0.35); }
        100% { box-shadow: 0 0 20px rgba(45,212,191,0.06), 0 0 40px rgba(45,212,191,0.03); border-color: rgba(45,212,191,0.15); }
    }
    .canvas-panel {
        background: rgba(45,212,191,0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(45,212,191,0.15);
        border-radius: 0.75rem;
        padding: 1.25rem;
        min-height: 480px;
        animation: canvasPulse 3s ease-in-out infinite;
    }
    .canvas-panel, .canvas-panel p, .canvas-panel li,
    .canvas-panel span, .canvas-panel strong, .canvas-panel b { color: #E8ECF1 !important; }
    .canvas-panel .stCaption *, .canvas-panel [data-testid="stCaptionContainer"] * { color: #8B95A5 !important; }
    .canvas-panel hr { border-color: rgba(255,255,255,0.08) !important; }
    .canvas-panel [data-testid="stMetric"] {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: none;
    }
    .canvas-panel [data-testid="stMetric"] label { color: #8B95A5 !important; }
    .canvas-panel [data-testid="stMetric"] [data-testid="stMetricValue"] { color: #2DD4BF !important; }
    .canvas-panel .stDownloadButton button {
        background: rgba(255,255,255,0.06) !important;
        color: #E8ECF1 !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
    }
    .canvas-panel .stDownloadButton button:hover { background: rgba(255,255,255,0.10) !important; }
    .canvas-panel .streamlit-expanderHeader,
    .canvas-panel .streamlit-expanderHeader p { background: rgba(255,255,255,0.04) !important; color: #E8ECF1 !important; }

    /* ── LIVE CANVAS label — pulsing glow ───────────── */
    @keyframes labelPulse {
        0%   { text-shadow: 0 0 8px rgba(45,212,191,0.5), 0 0 16px rgba(45,212,191,0.25); }
        50%  { text-shadow: 0 0 14px rgba(45,212,191,0.8), 0 0 28px rgba(45,212,191,0.4); }
        100% { text-shadow: 0 0 8px rgba(45,212,191,0.5), 0 0 16px rgba(45,212,191,0.25); }
    }
    .canvas-label {
        font-size: 0.95rem;
        font-weight: 700;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #2DD4BF !important;
        margin-bottom: 0.1rem;
        animation: labelPulse 2s ease-in-out infinite;
    }
    .canvas-heading {
        font-size: 1.15rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        color: #E8ECF1 !important;
        margin-bottom: 0.25rem;
        line-height: 1.3;
    }
    .canvas-explain {
        color: #8B95A5 !important;
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 0.8rem;
    }
    .canvas-body {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 0.5rem;
        padding: 0.8rem 1rem;
        font-size: 1rem;
        color: #E8ECF1;
        line-height: 1.6;
    }

    /* ── Step badge ──────────────────────────────────── */
    .step-badge {
        display: inline-block;
        background: rgba(45,212,191,0.08);
        color: #2DD4BF;
        padding: 0.2rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.88rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }

    /* ── Expander / Tabs / Alerts ────────────────────── */
    .streamlit-expanderHeader { background: rgba(255,255,255,0.04) !important; border-radius: 0.5rem !important; color: #E8ECF1 !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 0.5rem; }
    .stTabs [data-baseweb="tab"] { color: #8B95A5 !important; }
    .stTabs [aria-selected="true"] { color: #2DD4BF !important; border-bottom-color: #2DD4BF !important; }
    .stCodeBlock { border-radius: 0.5rem !important; }
    .stAlert { border-radius: 0.5rem !important; }
    hr { border-color: rgba(255,255,255,0.08) !important; }

    /* ── Buttons ─────────────────────────────────────── */
    .stDownloadButton button {
        background: linear-gradient(135deg, #2DD4BF 0%, #22D3EE 100%) !important;
        color: #06080D !important; border: none !important;
        border-radius: 0.5rem !important; font-weight: 600 !important;
    }
    .stFormSubmitButton button {
        background: linear-gradient(135deg, #2DD4BF 0%, #22D3EE 100%) !important;
        color: #06080D !important; border: none !important;
        border-radius: 0.5rem !important; font-weight: 600 !important;
        padding: 0.5rem 2rem !important;
    }
    .stButton > button {
        border: 1px solid rgba(255,255,255,0.12) !important;
        color: #2DD4BF !important;
        border-radius: 0.5rem !important;
        background: transparent !important;
        font-size: 1.05rem !important;
        padding: 0.5rem 1.5rem !important;
    }
    .stButton > button:hover {
        background: rgba(45,212,191,0.08) !important;
        border-color: #2DD4BF !important;
    }

    /* ═══════════════════════════════════════════════════
       LANDING PAGE
       ═══════════════════════════════════════════════════ */
    .landing {
        text-align: center;
        padding: 6rem 1rem 2rem 1rem;
    }
    .landing-icon {
        font-size: 5rem;
        margin-bottom: 1rem;
        display: block;
        filter: drop-shadow(0 0 20px rgba(45,212,191,0.4));
    }
    .landing h1 {
        font-size: 2.5rem !important;
        letter-spacing: 0.08em;
        margin-bottom: 0.8rem !important;
    }
    .landing-sub {
        font-size: 1.15rem;
        color: #8B95A5;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.7;
    }

    /* ═══════════════════════════════════════════════════
       GUIDE PAGES (sidebar + canvas explainers)
       ═══════════════════════════════════════════════════ */
    .guide-page {
        text-align: center;
        padding: 2rem 0 1rem 0;
    }
    .guide-step-num {
        font-size: 0.85rem;
        letter-spacing: 0.15em;
        color: #5A6478;
        margin-bottom: 0.3rem;
    }
    .guide-page h2 {
        text-align: center;
        margin-bottom: 0.5rem !important;
    }
    .guide-panel {
        background: rgba(255,255,255,0.04);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 0.75rem;
        padding: 1.5rem;
        min-height: 280px;
    }
    .guide-panel p, .guide-panel li {
        font-size: 1.08rem !important;
        line-height: 1.7 !important;
        color: #C8D0DC !important;
    }
    .guide-panel b { color: #E8ECF1 !important; }
    .guide-panel-label {
        font-size: 0.75rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #2DD4BF;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }

    /* ═══════════════════════════════════════════════════
       DASHBOARD — journey + deliverables
       ═══════════════════════════════════════════════════ */
    .journey-list { margin: 0.4rem 0; }
    .journey-item {
        display: flex;
        align-items: baseline;
        gap: 0.6rem;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        font-size: 1.05rem;
        line-height: 1.5;
    }
    .journey-item:last-child { border-bottom: none; }
    .journey-num {
        flex-shrink: 0;
        width: 26px; height: 26px;
        border-radius: 50%;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        color: #8B95A5 !important;
        display: inline-flex;
        align-items: center; justify-content: center;
        font-size: 0.75rem; font-weight: 600;
    }
    .journey-num.done {
        background: rgba(45,212,191,0.10);
        border-color: #2DD4BF;
        color: #2DD4BF !important;
    }
    .journey-name { font-weight: 600; min-width: 140px; color: #E8ECF1; }
    .journey-desc { color: #8B95A5; font-size: 0.98rem; }
    .deliv-row { display: flex; gap: 0.75rem; margin: 0.4rem 0; }
    .deliv-item {
        flex: 1;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 0.5rem;
        padding: 0.75rem 0.9rem;
        font-size: 0.95rem; line-height: 1.5;
        color: #8B95A5;
    }
    .deliv-item b { display: block; margin-bottom: 0.15rem; color: #E8ECF1; }

    /* ── Sidebar label ──────────────────────────────── */
    .sidebar-label {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.14em;
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
