"""
Step 6: Transformations
Define transformation logic and processing steps.
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from state_manager import StateManager

StateManager.initialize()

st.header("Step 6: Transformations")
st.markdown("Define the transformation steps that produce your data product.")

transformations = StateManager.get("transformations", [])

with st.form("add_transformation_form"):
    st.subheader("Add a Transformation Step")
    step_name = st.text_input("Step Name")
    step_type = st.selectbox(
        "Transformation Type",
        options=["SQL", "Python", "dbt Model", "Spark", "Other"],
    )
    source_entity = st.text_input("Source Entity / Table")
    target_entity = st.text_input("Target Entity / Table")
    logic = st.text_area("Transformation Logic / SQL")
    description = st.text_area("Description")

    add_step = st.form_submit_button("Add Transformation")
    if add_step and step_name:
        transformations.append({
            "name": step_name,
            "type": step_type,
            "source_entity": source_entity,
            "target_entity": target_entity,
            "logic": logic,
            "description": description,
        })
        StateManager.set("transformations", transformations)
        StateManager.mark_step_completed("transformations")
        st.success(f"Transformation '{step_name}' added.")

if transformations:
    st.subheader("Defined Transformations")
    for i, t in enumerate(transformations):
        with st.expander(f"{i+1}. {t['name']} ({t['type']})"):
            st.write(f"**Source:** {t['source_entity']} → **Target:** {t['target_entity']}")
            st.write(f"**Description:** {t['description']}")
            if t["logic"]:
                st.code(t["logic"], language="sql")
else:
    st.info("No transformations defined yet.")
