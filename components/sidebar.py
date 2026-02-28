"""
Sidebar: progress tracker + step-specific contextual guide + glossary.
"""

import streamlit as st
from state_manager import get_progress
from components.helpers import STEP_GUIDES

GLOSSARY = {
    "Data Product": "A curated, governed dataset built for a specific business purpose.",
    "PII": "Personally Identifiable Information — data that can identify an individual.",
    "Classification": "A sensitivity label: Public, Internal, Confidential, or Restricted.",
    "Grain": "The level of detail in a table — what one row represents.",
    "SLA": "Service Level Agreement — expected timeliness of data delivery.",
    "dbt": "Data Build Tool — a transformation framework for analytics engineering.",
    "Lineage": "The path data follows from source to consumption.",
    "Retention Policy": "How long data is stored before archival or deletion.",
    "Data Domain": "A business area (e.g. Finance, Risk) that owns the data.",
    "Data Steward": "The person responsible for quality and governance of a data asset.",
    "DDL": "Data Definition Language — SQL that defines database structures.",
    "Masking Policy": "A rule that obfuscates sensitive columns for unauthorized users.",
}


def render_sidebar(step: int = None):
    """
    Render the sidebar with progress, step guide, and glossary.

    Args:
        step: Current step number (1-7). If provided, shows contextual guide.
    """
    product = st.session_state.product
    progress = get_progress(product)

    with st.sidebar:
        # ── Progress ────────────────────────────────────────────
        st.markdown("# 🏛️ Data Product Steward")
        st.progress(progress["pct"] / 100)
        st.caption(
            f"**{progress['pct']}%** complete — {progress['done']}/{progress['total']} steps"
        )

        st.divider()

        for step_name, done in progress["steps"].items():
            icon = "✅" if done else "⬜"
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

        # ── Glossary ───────────────────────────────────────────
        st.divider()
        with st.expander("📖 Glossary"):
            for term, defn in GLOSSARY.items():
                st.markdown(f"**{term}:** {defn}")
