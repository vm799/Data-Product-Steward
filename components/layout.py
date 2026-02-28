"""
Custom CSS and shared layout utilities for a modern, guided wizard experience.
"""

import streamlit as st

CUSTOM_CSS = """
<style>
    /* ── Base typography: bigger, more readable ─────────────── */
    .main .block-container {
        padding: 1.5rem 1.5rem 2rem 1.5rem;
        max-width: 100%;
    }
    [data-testid="stAppViewContainer"] > .main {
        font-size: 1.08rem;
        line-height: 1.65;
    }

    /* ── Stronger header hierarchy ──────────────────────────── */
    h1 {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em;
    }
    h2 {
        font-size: 1.55rem !important;
        font-weight: 600 !important;
    }
    h3 {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
    }

    /* ── Form labels: bigger and bolder ─────────────────────── */
    .stTextInput label p,
    .stSelectbox label p,
    .stMultiSelect label p,
    .stTextArea label p,
    .stSlider label p,
    .stNumberInput label p,
    .stCheckbox label p {
        font-size: 1.02rem !important;
        font-weight: 500 !important;
    }

    /* ── Metric cards: subtle background ────────────────────── */
    [data-testid="stMetric"] {
        background: #f8f9fb;
        padding: 0.75rem 1rem;
        border-radius: 0.6rem;
        border: 1px solid #e8eaed;
    }

    /* ── Sidebar refinements ────────────────────────────────── */
    section[data-testid="stSidebar"] {
        font-size: 1rem;
    }
    section[data-testid="stSidebar"] h1 {
        font-size: 1.4rem !important;
    }
    section[data-testid="stSidebar"] h3 {
        font-size: 1.15rem !important;
    }

    /* ── Step badge ─────────────────────────────────────────── */
    .step-badge {
        display: inline-block;
        background: #e8f0fe;
        color: #1a73e8;
        padding: 0.2rem 0.7rem;
        border-radius: 1rem;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }

    /* ── Canvas section ─────────────────────────────────────── */
    .canvas-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.6rem 1rem;
        border-radius: 0.5rem 0.5rem 0 0;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0;
    }
    .canvas-body {
        background: #fafbfc;
        border: 1px solid #e0e3e8;
        border-top: none;
        border-radius: 0 0 0.5rem 0.5rem;
        padding: 0.8rem 1rem;
        font-size: 0.95rem;
    }

    /* ── Guide card in sidebar ──────────────────────────────── */
    .guide-card {
        background: #f0f7ff;
        border-left: 3px solid #1a73e8;
        padding: 0.8rem;
        border-radius: 0 0.4rem 0.4rem 0;
        font-size: 0.92rem;
        line-height: 1.55;
        margin-bottom: 0.5rem;
    }

    /* ── Deliverable row ────────────────────────────────────── */
    .deliverable-row {
        padding: 0.25rem 0;
        font-size: 0.92rem;
    }
</style>
"""


def inject_custom_css():
    """Inject the custom CSS into the page. Call once at the top of every page."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def step_header(step_num: int, title: str, subtitle: str):
    """Render a consistent step header with step badge."""
    st.markdown(
        f'<span class="step-badge">Step {step_num} of 7</span>',
        unsafe_allow_html=True,
    )
    st.header(title)
    st.caption(subtitle)
