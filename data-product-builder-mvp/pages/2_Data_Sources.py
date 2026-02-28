"""
Step 2: Data Sources
Identify and configure source systems feeding the data product.
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from state_manager import StateManager

StateManager.initialize()

st.header("Step 2: Data Sources")
st.markdown("Add the source systems and datasets that feed this data product.")

sources = StateManager.get("data_sources", [])

with st.form("add_source_form"):
    st.subheader("Add a Data Source")
    source_name = st.text_input("Source Name")
    source_type = st.selectbox(
        "Source Type",
        options=["Database", "API", "File (CSV/Parquet)", "Streaming", "Data Lake", "Other"],
    )
    connection_details = st.text_area("Connection Details / Description")
    schema_name = st.text_input("Schema / Dataset Name")
    refresh_frequency = st.selectbox(
        "Refresh Frequency",
        options=["Real-time", "Hourly", "Daily", "Weekly", "Monthly", "On-demand"],
    )

    add_source = st.form_submit_button("Add Source")
    if add_source and source_name:
        sources.append({
            "name": source_name,
            "type": source_type,
            "connection_details": connection_details,
            "schema": schema_name,
            "refresh_frequency": refresh_frequency,
        })
        StateManager.set("data_sources", sources)
        StateManager.mark_step_completed("data_sources")
        st.success(f"Source '{source_name}' added.")

if sources:
    st.subheader("Registered Sources")
    for i, src in enumerate(sources):
        st.markdown(f"**{i+1}. {src['name']}** — {src['type']} ({src['refresh_frequency']})")
else:
    st.info("No data sources added yet.")
