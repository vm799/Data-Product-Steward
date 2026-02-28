"""
Step 5: Data Quality
Set data quality rules, thresholds, and monitoring expectations.
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from state_manager import StateManager
from config import QUALITY_THRESHOLDS

StateManager.initialize()

st.header("Step 5: Data Quality")
st.markdown("Define quality expectations and validation rules for your data product.")

dq = StateManager.get("data_quality", {})

with st.form("data_quality_form"):
    completeness = st.slider(
        "Completeness Threshold (%)",
        min_value=0,
        max_value=100,
        value=int(dq.get("completeness", QUALITY_THRESHOLDS["completeness"]) * 100),
    )
    accuracy = st.slider(
        "Accuracy Threshold (%)",
        min_value=0,
        max_value=100,
        value=int(dq.get("accuracy", QUALITY_THRESHOLDS["accuracy"]) * 100),
    )
    timeliness_hours = st.number_input(
        "Timeliness SLA (hours)",
        min_value=1,
        max_value=720,
        value=dq.get("timeliness_hours", QUALITY_THRESHOLDS["timeliness_hours"]),
    )
    uniqueness = st.slider(
        "Uniqueness Threshold (%)",
        min_value=0,
        max_value=100,
        value=int(dq.get("uniqueness", QUALITY_THRESHOLDS["uniqueness"]) * 100),
    )
    custom_rules = st.text_area(
        "Custom Quality Rules (one per line)",
        value=dq.get("custom_rules", ""),
    )
    monitoring_channel = st.text_input(
        "Alerting Channel (e.g., Slack channel, email)",
        value=dq.get("monitoring_channel", ""),
    )

    submitted = st.form_submit_button("Save Quality Rules")
    if submitted:
        StateManager.set("data_quality", {
            "completeness": completeness / 100,
            "accuracy": accuracy / 100,
            "timeliness_hours": timeliness_hours,
            "uniqueness": uniqueness / 100,
            "custom_rules": custom_rules,
            "monitoring_channel": monitoring_channel,
        })
        StateManager.mark_step_completed("data_quality")
        st.success("Data quality rules saved.")
