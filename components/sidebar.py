"""
Sidebar: progress tracker, page tree navigation, glossary.
Aligned with Collibra brand colors and design.
"""

import streamlit as st
from state_manager import get_progress, get_next_step
from components.helpers import STEP_GUIDES, PAGE_MAP, STEP_NAMES


# ── Glossary: each term is individually expandable ─────────────────
GLOSSARY = {
    "Data Product": (
        "A curated, governed dataset built for a specific business purpose — "
        "e.g. an Investor Position Summary or a Risk Exposure Feed."
    ),
    "PII": (
        "Personally Identifiable Information — any data that can identify "
        "a real person (name, SSN, email, account number). Triggers masking "
        "policies and stricter access controls automatically."
    ),
    "Classification": (
        "Sensitivity label that controls access: "
        "Public, Internal, Confidential, or Restricted. Determines who "
        "can see the data and what security controls are applied."
    ),
    "Grain": (
        "The level of detail in a table — what one row represents. "
        "e.g. one row per trade, per customer, or per day."
    ),
    "SLA": (
        "Service Level Agreement — how quickly data must arrive. "
        "e.g. 'refreshed within 4 hours of market close'."
    ),
    "dbt": (
        "Data Build Tool — industry-standard framework for writing "
        "and testing SQL transformations. The wizard generates "
        "schema.yml and staging models you can deploy directly."
    ),
    "Lineage": (
        "The documented path data follows from source to consumption — "
        "regulators require this for audit trails."
    ),
    "DDL": (
        "Data Definition Language — SQL commands (CREATE TABLE, ALTER, "
        "GRANT) that define Snowflake database structures."
    ),
    "Masking Policy": (
        "A Snowflake rule that hides sensitive column values "
        "from unauthorized users automatically. Auto-generated "
        "when you tag columns as PII."
    ),
    "Retention Policy": (
        "How long data is kept before archival or deletion. "
        "Regulated firms typically need 3-7 years."
    ),
    "Data Domain": (
        "A business area that owns the data — Finance, Risk, "
        "Trading, HR, Operations."
    ),
    "Data Steward": (
        "The named person responsible for quality and governance "
        "of a data asset. Every product needs one."
    ),
    "Secure View": (
        "A Snowflake view with row-level security that restricts "
        "which rows a user can see based on their role."
    ),
    "Collibra": (
        "A data governance catalogue. The wizard exports a JSON "
        "import file with all your product metadata."
    ),
}


def render_sidebar(step: int = None):
    """Render sidebar with progress, page tree, and glossary."""
    product = st.session_state.product
    progress = get_progress(product)
    next_step = get_next_step(product)

    with st.sidebar:
        # ── Dashboard ─────────────────────────────────────
        st.page_link("streamlit_app.py", label="Dashboard")

        st.divider()

        # ══════════════════════════════════════════════════
        # PROGRESS TRACKER
        # ══════════════════════════════════════════════════
        st.progress(progress["pct"] / 100)
        st.caption(
            f"**{progress['pct']}%** complete — "
            f"{progress['done']}/{progress['total']} steps"
        )

        st.divider()

        # ══════════════════════════════════════════════════
        # PAGE TREE — clickable navigation
        # ══════════════════════════════════════════════════
        step_names = list(progress["steps"].keys())
        for i, step_name in enumerate(step_names, 1):
            done = progress["steps"][step_name]
            is_current = step is not None and i == step
            is_next = i == next_step

            if done:
                prefix = f"{i}. "
            else:
                prefix = f"{i}. "

            st.page_link(PAGE_MAP[i], label=f"{prefix}{step_name}")

        # ── Canvas link ───────────────────────────────────
        st.page_link(
            "pages/8_Product_Canvas.py",
            label="Product Canvas",
        )

        # ══════════════════════════════════════════════════
        # STEP GUIDE — context-sensitive tips
        # ══════════════════════════════════════════════════
        if step is not None and step in STEP_GUIDES:
            st.divider()
            guide = STEP_GUIDES[step]
            st.markdown(f"**{guide['title']}**")
            st.caption(guide["why"])
            for tip in guide["tips"]:
                st.caption(f"- {tip}")

        # ══════════════════════════════════════════════════
        # GLOSSARY — each term individually expandable
        # ══════════════════════════════════════════════════
        st.divider()
        st.caption("**GLOSSARY** — click a term to learn more")

        for term, definition in GLOSSARY.items():
            with st.expander(term, expanded=False):
                st.markdown(definition)
