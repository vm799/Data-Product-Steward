"""
Sidebar: orientation label, theme toggle, progress tracker,
step-specific guide, and glossary.

Designed so a first-time user immediately understands what the sidebar is for.
"""

import streamlit as st
from state_manager import get_progress
from components.helpers import STEP_GUIDES

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
        "A sensitivity label that controls who can see the data: "
        "Public, Internal, Confidential, or Restricted."
    ),
    "Grain": "The level of detail in a table — what one row represents.",
    "SLA": (
        "Service Level Agreement — how quickly data must arrive. "
        "e.g. 'refreshed within 4 hours of market close'."
    ),
    "dbt": (
        "Data Build Tool — an industry-standard framework for writing "
        "and testing data transformations in SQL."
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
        "A business area that owns the data — e.g. Finance, Risk, "
        "Trading, HR, Operations."
    ),
    "Data Steward": (
        "The named person responsible for the quality and governance "
        "of a data asset. Every product needs one."
    ),
    "DDL": (
        "Data Definition Language — SQL commands (CREATE TABLE, etc.) "
        "that define database structures in Snowflake."
    ),
    "Masking Policy": (
        "A Snowflake security rule that automatically hides sensitive "
        "column values from unauthorized users."
    ),
}


def render_sidebar(step: int = None):
    """
    Render the sidebar with orientation, theme toggle, progress,
    step guide, and glossary.

    Args:
        step: Current step number (1-7). If provided, shows contextual guide.
    """
    product = st.session_state.product
    progress = get_progress(product)

    with st.sidebar:
        # ── Theme toggle ───────────────────────────────────────
        st.toggle("🌙 Dark Mode", key="dark_mode")

        st.divider()

        # ── Branding + orientation ─────────────────────────────
        st.markdown("# 📊 Data Product Builder")
        st.caption(
            "This sidebar tracks your progress, shows tips for each step, "
            "and provides a glossary. Use the page links above to navigate."
        )

        st.divider()

        # ── Progress tracker ───────────────────────────────────
        st.markdown("### Your Progress")
        st.progress(progress["pct"] / 100)
        st.caption(
            f"**{progress['pct']}%** complete — "
            f"{progress['done']}/{progress['total']} steps done"
        )

        # Step checklist
        step_names = list(progress["steps"].keys())
        for i, step_name in enumerate(step_names, 1):
            done = progress["steps"][step_name]
            icon = "✅" if done else "⬜"
            # Highlight current step
            if step is not None and i == step:
                st.markdown(f"**{icon} ▶ {step_name}** ← you are here")
            else:
                st.markdown(f"{icon} {step_name}")

        # ── Step Guide (contextual) ────────────────────────────
        if step is not None and step in STEP_GUIDES:
            st.divider()
            guide = STEP_GUIDES[step]

            st.markdown(f"### 💡 {guide['title']}")
            st.markdown(
                f'<div class="guide-card">{guide["why"]}</div>',
                unsafe_allow_html=True,
            )
            st.markdown("**Tips:**")
            for tip in guide["tips"]:
                st.markdown(f"- {tip}")

            st.caption(f"Feeds into: {guide['feeds']}")
        elif step is None:
            # Home page — show general orientation
            st.divider()
            st.markdown("### 💡 Getting Started")
            st.markdown(
                '<div class="guide-card">'
                "Click <b>Business Context</b> in the page list above to begin "
                "building your data product. Each step builds on the last — "
                "work through them in order for the best results."
                "</div>",
                unsafe_allow_html=True,
            )

        # ── Glossary ───────────────────────────────────────────
        st.divider()
        st.markdown("### 📖 Glossary")
        st.caption("Key terms explained — expand to look up any unfamiliar concept.")

        with st.expander("Open Glossary", expanded=False):
            for term, defn in GLOSSARY.items():
                st.markdown(f"**{term}:** {defn}")
