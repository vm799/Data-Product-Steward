"""
Step 7: Review & Export
Review the complete data product definition and export artifacts.
"""

import json
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from state_manager import StateManager

StateManager.initialize()

st.header("Step 7: Review & Export")
st.markdown("Review your data product definition and export artifacts.")

# Progress overview
progress = StateManager.get_overall_progress()
st.metric("Completion", f"{progress}%")
st.progress(progress / 100)

# Step-by-step review
completed = st.session_state.get("step_completed", {})
st.subheader("Step Completion Status")
for step_key, is_done in completed.items():
    icon = "✅" if is_done else "⬜"
    st.markdown(f"{icon} **{step_key.replace('_', ' ').title()}**")

# Full state preview
st.subheader("Data Product Definition")
snapshot = StateManager.get_state_snapshot()
with st.expander("View Full JSON"):
    st.json(snapshot)

# Export
st.subheader("Export")
json_str = json.dumps(snapshot, indent=2, default=str)
st.download_button(
    label="Download as JSON",
    data=json_str,
    file_name="data_product_definition.json",
    mime="application/json",
)

if progress == 100:
    st.success("All steps are complete. Your data product is ready for export.")
else:
    st.warning("Some steps are incomplete. Complete all steps for a full export.")
