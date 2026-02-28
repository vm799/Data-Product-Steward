import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from state_manager import initialize_state, mark_step_complete
from components.sidebar import render_sidebar
from config import QUALITY_THRESHOLDS

initialize_state()
render_sidebar()

st.header("5️⃣ Data Quality")
st.caption("Configure quality thresholds, validation rules, and monitoring.")

product = st.session_state.product
qr = product.get("quality_rules", {})

with st.form("data_quality_form"):
    col1, col2 = st.columns(2)

    with col1:
        completeness = st.slider(
            "Completeness Threshold (%)",
            min_value=0,
            max_value=100,
            value=qr.get("completeness", QUALITY_THRESHOLDS["completeness"]),
        )
        accuracy = st.slider(
            "Accuracy Threshold (%)",
            min_value=0,
            max_value=100,
            value=qr.get("accuracy", QUALITY_THRESHOLDS["accuracy"]),
        )
        timeliness_hours = st.number_input(
            "Timeliness SLA (hours)",
            min_value=1,
            max_value=720,
            value=qr.get("timeliness_hours", QUALITY_THRESHOLDS["timeliness_hours"]),
        )

    with col2:
        uniqueness = st.slider(
            "Uniqueness Threshold (%)",
            min_value=0,
            max_value=100,
            value=qr.get("uniqueness", QUALITY_THRESHOLDS["uniqueness"]),
        )
        custom_rules = st.text_area(
            "Custom Quality Rules (one per line)",
            value=qr.get("custom_rules", ""),
            help="E.g. INVESTOR_ID must not be null\nEMAIL must match regex pattern",
        )
        monitoring_channel = st.text_input(
            "Alerting Channel",
            value=qr.get("monitoring_channel", ""),
            help="E.g. #data-quality-alerts, data-team@firm.com",
        )

    submitted = st.form_submit_button("Save Quality Rules")

    if submitted:
        product["quality_rules"] = {
            "completeness": completeness,
            "accuracy": accuracy,
            "timeliness_hours": timeliness_hours,
            "uniqueness": uniqueness,
            "custom_rules": custom_rules,
            "monitoring_channel": monitoring_channel,
        }
        mark_step_complete("quality")
        st.success("Data quality rules saved.")

# Quality summary
st.divider()
st.subheader("📊 Quality Profile")

saved = product.get("quality_rules", {})
if saved:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Completeness", f"{saved.get('completeness', '—')}%")
    c2.metric("Accuracy", f"{saved.get('accuracy', '—')}%")
    c3.metric("Timeliness", f"{saved.get('timeliness_hours', '—')}h")
    c4.metric("Uniqueness", f"{saved.get('uniqueness', '—')}%")
else:
    st.info("No quality rules saved yet. Fill in the form above.")
