"""
Sidebar: progress tracker, clickable step navigation, step guide, glossary.
Glass panel on dark gradient — always dark theme.
"""

import streamlit as st
from state_manager import get_progress, get_next_step
from components.helpers import STEP_GUIDES, PAGE_MAP, STEP_NAMES

GLOSSARY = {
    "Data Product": (
        "A curated, governed dataset built for a specific business purpose — "
        "e.g. an Investor Position Summary or a Risk Exposure Feed."
    ),
    "PII": (
        "Personally Identifiable Information — any data that can identify "
        "a real person (name, SSN, email, account number)."
    ),
    "Classification": (
        "Sensitivity label that controls access: "
        "Public, Internal, Confidential, or Restricted."
    ),
    "Grain": "The level of detail in a table — what one row represents.",
    "SLA": (
        "Service Level Agreement — how quickly data must arrive. "
        "e.g. 'refreshed within 4 hours of market close'."
    ),
    "dbt": (
        "Data Build Tool — industry-standard framework for writing "
        "and testing SQL transformations."
    ),
    "Lineage": (
        "The documented path data follows from source to consumption — "
        "regulators require this for audit."
    ),
    "Retention Policy": (
        "How long data is kept before archival or deletion. "
        "Regulated firms typically need 3–7 years."
    ),
    "Data Domain": (
        "A business area that owns the data — Finance, Risk, "
        "Trading, HR, Operations."
    ),
    "Data Steward": (
        "The named person responsible for quality and governance "
        "of a data asset. Every product needs one."
    ),
    "DDL": (
        "Data Definition Language — SQL commands (CREATE TABLE, etc.) "
        "that define Snowflake structures."
    ),
    "Masking Policy": (
        "A Snowflake rule that hides sensitive column values "
        "from unauthorized users automatically."
    ),
}


def render_sidebar(step: int = None):
    """Render sidebar with progress, clickable steps, guide, and glossary."""
    product = st.session_state.product
    progress = get_progress(product)
    next_step = get_next_step(product)

    with st.sidebar:
        # ── Dashboard link — always at top ────────────────
        st.page_link("streamlit_app.py", label="⌂ DASHBOARD")

        st.markdown(
            '<div class="sidebar-label">// navigation & tools</div>',
            unsafe_allow_html=True,
        )
        st.caption("Click any step to navigate. Progress saves automatically.")

        st.divider()

        # ── Progress ───────────────────────────────────────
        st.markdown("### Progress")
        st.progress(progress["pct"] / 100)
        st.caption(
            f"**{progress['pct']}%** — "
            f"{progress['done']}/{progress['total']} steps"
        )

        # ── Clickable step list ────────────────────────────
        step_names = list(progress["steps"].keys())
        for i, step_name in enumerate(step_names, 1):
            done = progress["steps"][step_name]
            icon = "✅" if done else "⬜"
            is_current = step is not None and i == step
            is_next = i == next_step

            if is_current:
                label = f"{icon} ▶ {step_name}"
            elif is_next:
                label = f"🔶 {step_name}"
            else:
                label = f"{icon} {step_name}"

            st.page_link(PAGE_MAP[i], label=label)

        # ── Step guide ─────────────────────────────────────
        if step is not None and step in STEP_GUIDES:
            st.divider()
            guide = STEP_GUIDES[step]
            st.markdown(f"### {guide['title']}")
            st.markdown(
                f'<div class="guide-card">{guide["why"]}</div>',
                unsafe_allow_html=True,
            )
            st.markdown("**Tips:**")
            for tip in guide["tips"]:
                st.markdown(f"- {tip}")
            st.caption(f"Feeds into: {guide['feeds']}")
        elif step is None:
            st.divider()
            st.markdown("### Getting Started")
            st.markdown(
                '<div class="guide-card">'
                "Select <b>Business Context</b> above to begin. "
                "Each step builds on the last — work through them in order."
                "</div>",
                unsafe_allow_html=True,
            )

        # ── Glossary ───────────────────────────────────────
        st.divider()
        st.markdown("### Glossary")
        st.caption("Key terms — expand to look up unfamiliar concepts.")
        with st.expander("Open Glossary", expanded=False):
            for term, defn in GLOSSARY.items():
                st.markdown(f"**{term}:** {defn}")
