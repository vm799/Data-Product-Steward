import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from state_manager import initialize_state
from components.sidebar import render_sidebar

initialize_state()
render_sidebar()

st.header("6️⃣ Transformations")
st.caption("Define the processing steps that produce your data product.")

product = st.session_state.product

if "transformations" not in product:
    product["transformations"] = []

st.subheader("Add Transformation Step")

with st.form("add_transformation_form"):
    step_name = st.text_input("Step Name")

    col1, col2 = st.columns(2)

    with col1:
        step_type = st.selectbox(
            "Transformation Type",
            ["SQL", "Python", "dbt Model", "Spark", "Other"],
        )
        source_entity = st.text_input("Source Entity / Table")
        target_entity = st.text_input("Target Entity / Table")

    with col2:
        description = st.text_area("Description")
        logic = st.text_area("Transformation Logic / SQL")

    submitted = st.form_submit_button("Add Transformation")

    if submitted:
        if not step_name:
            st.error("Step name is required.")
        else:
            product["transformations"].append({
                "name": step_name,
                "type": step_type,
                "source_entity": source_entity,
                "target_entity": target_entity,
                "logic": logic,
                "description": description,
            })
            st.success(f"Transformation **{step_name}** added.")

# Display transformations
st.subheader("Defined Transformations")

if product["transformations"]:
    for i, t in enumerate(product["transformations"]):
        with st.expander(f"⚙️ {t['name']} ({t['type']})"):
            st.markdown(f"**Source:** `{t['source_entity']}` → **Target:** `{t['target_entity']}`")
            if t.get("description"):
                st.markdown(f"**Description:** {t['description']}")
            if t.get("logic"):
                st.code(t["logic"], language="sql")

            if st.button("Remove", key=f"rm_tx_{i}"):
                product["transformations"].pop(i)
                st.rerun()
else:
    st.info("No transformations defined yet.")
