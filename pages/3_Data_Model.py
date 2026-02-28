import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from state_manager import initialize_state
from components.sidebar import render_sidebar

initialize_state()
render_sidebar()

st.header("3️⃣ Data Model Builder")
st.caption("Define entities, attributes, data types, and PII classification.")

product = st.session_state.product

if "entities" not in product:
    product["entities"] = []

st.subheader("Create New Entity")

entity_name = st.text_input("Entity Name (Table Name)")
create_entity = st.button("Add Entity")

if create_entity:
    if not entity_name:
        st.error("Entity name required.")
    else:
        entity = {"name": entity_name.upper(), "attributes": []}
        product["entities"].append(entity)
        st.success(f"Entity **{entity_name.upper()}** created.")

st.divider()

# Display Existing Entities
for idx, entity in enumerate(product["entities"]):
    with st.expander(f"📦 {entity['name']} ({len(entity['attributes'])} attributes)", expanded=True):

        st.markdown("#### Add Attribute")

        with st.form(f"add_attr_{entity['name']}"):
            col1, col2 = st.columns(2)

            with col1:
                attr_name = st.text_input("Attribute Name")
                data_type = st.selectbox(
                    "Data Type",
                    ["STRING", "NUMBER", "FLOAT", "BOOLEAN", "DATE", "TIMESTAMP"],
                )
                nullable = st.checkbox("Nullable?", value=True)

            with col2:
                contains_pii = st.checkbox("Contains PII?")
                description = st.text_input("Description")

            submitted = st.form_submit_button("Add Attribute")

            if submitted:
                if not attr_name:
                    st.error("Attribute name required.")
                else:
                    attribute = {
                        "name": attr_name.upper(),
                        "data_type": data_type,
                        "nullable": nullable,
                        "pii": contains_pii,
                        "description": description,
                    }
                    entity["attributes"].append(attribute)
                    if contains_pii:
                        product["pii"] = True
                    st.success(f"Attribute **{attr_name.upper()}** added.")

        # Attribute table
        if entity["attributes"]:
            st.markdown("#### Current Attributes")
            for j, attr in enumerate(entity["attributes"]):
                pii_badge = " 🔴 PII" if attr.get("pii") else ""
                null_badge = "NULL" if attr.get("nullable") else "NOT NULL"
                st.markdown(
                    f"- `{attr['name']}` · {attr['data_type']} · {null_badge}{pii_badge}"
                    + (f" — _{attr['description']}_" if attr.get("description") else "")
                )
        else:
            st.info("No attributes yet. Add at least one attribute.")

        if st.button(f"Remove Entity", key=f"rm_ent_{idx}"):
            product["entities"].pop(idx)
            st.rerun()
