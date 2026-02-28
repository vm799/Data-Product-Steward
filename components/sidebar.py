import streamlit as st
from state_manager import get_progress

GLOSSARY = {
    "Data Product": "A curated, governed dataset designed for a specific business purpose.",
    "PII": "Personally Identifiable Information — data that can identify an individual.",
    "Classification": "A label (Public, Internal, Confidential, Restricted) indicating sensitivity.",
    "Grain": "The level of detail in a table — what one row represents.",
    "SLA": "Service Level Agreement — the expected timeliness of data delivery.",
    "dbt": "Data Build Tool — a transformation framework for analytics engineering.",
    "Lineage": "The path data follows from source to consumption.",
    "Retention Policy": "How long data is stored before archival or deletion.",
    "Data Domain": "A business area (e.g., Finance, Risk) that owns the data.",
    "Data Steward": "A person responsible for the quality and governance of a data asset.",
    "DDL": "Data Definition Language — SQL statements that define database structures.",
    "Masking Policy": "A rule that obfuscates sensitive data for unauthorized users.",
}


def render_sidebar():
    """Render the shared sidebar with progress tracker and glossary."""
    product = st.session_state.product
    progress = get_progress(product)

    with st.sidebar:
        st.markdown("### 🏛️ GDP Data Product Steward")
        st.progress(progress["pct"] / 100)
        st.caption(f"**{progress['pct']}%** complete — {progress['done']}/{progress['total']} steps")

        st.divider()

        for step_name, done in progress["steps"].items():
            icon = "✅" if done else "⬜"
            st.markdown(f"{icon} {step_name}")

        st.divider()

        with st.expander("📖 Glossary"):
            for term, definition in GLOSSARY.items():
                st.markdown(f"**{term}:** {definition}")
