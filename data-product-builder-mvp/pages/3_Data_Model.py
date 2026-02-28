"""
Step 3: Data Model
Design the target schema and entity relationships for the data product.
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from state_manager import StateManager

StateManager.initialize()

st.header("Step 3: Data Model")
st.markdown("Define the target schema, entities, and relationships.")

data_model = StateManager.get("data_model", {})
entities = data_model.get("entities", [])

with st.form("add_entity_form"):
    st.subheader("Add an Entity")
    entity_name = st.text_input("Entity / Table Name")
    entity_description = st.text_area("Entity Description")
    columns_raw = st.text_area(
        "Columns (name:type per line, e.g. customer_id:INTEGER)",
        help="Enter one column per line in name:type format.",
    )
    primary_key = st.text_input("Primary Key Column")
    grain = st.text_input("Grain (e.g., one row per customer per day)")

    add_entity = st.form_submit_button("Add Entity")
    if add_entity and entity_name:
        columns = []
        for line in columns_raw.strip().splitlines():
            parts = line.split(":")
            if len(parts) == 2:
                columns.append({"name": parts[0].strip(), "type": parts[1].strip()})
        entities.append({
            "name": entity_name,
            "description": entity_description,
            "columns": columns,
            "primary_key": primary_key,
            "grain": grain,
        })
        data_model["entities"] = entities
        StateManager.set("data_model", data_model)
        StateManager.mark_step_completed("data_model")
        st.success(f"Entity '{entity_name}' added.")

if entities:
    st.subheader("Defined Entities")
    for ent in entities:
        with st.expander(ent["name"]):
            st.write(f"**Description:** {ent['description']}")
            st.write(f"**Primary Key:** {ent['primary_key']}")
            st.write(f"**Grain:** {ent['grain']}")
            if ent["columns"]:
                st.table(ent["columns"])
else:
    st.info("No entities defined yet.")
