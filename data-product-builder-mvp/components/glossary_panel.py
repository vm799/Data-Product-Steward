"""
Glossary Panel Component
Displays a contextual glossary of data product terms in the sidebar or main area.
"""

import streamlit as st

GLOSSARY = {
    "Data Product": "A curated, governed dataset designed for a specific business purpose.",
    "PII": "Personally Identifiable Information — data that can identify an individual.",
    "Data Classification": "A label (Public, Internal, Confidential, Restricted) indicating sensitivity.",
    "Grain": "The level of detail in a table — what one row represents.",
    "SLA": "Service Level Agreement — the expected timeliness of data delivery.",
    "dbt": "Data Build Tool — a transformation framework for analytics engineering.",
    "Lineage": "The path data follows from source to consumption.",
    "Retention Policy": "How long data is stored before archival or deletion.",
    "Data Domain": "A business area (e.g., Finance, Marketing) that owns the data.",
    "Data Steward": "A person responsible for the quality and governance of a data asset.",
}


def render_glossary():
    """Render the glossary panel."""
    st.subheader("Glossary")
    for term, definition in GLOSSARY.items():
        with st.expander(term):
            st.write(definition)
