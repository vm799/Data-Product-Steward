import streamlit as st

st.header("3️⃣ Data Model Builder")

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
        entity = {
            "name": entity_name.upper(),
            "attributes": []
        }
        product["entities"].append(entity)
        st.success(f"Entity {entity_name} created.")

st.divider()

# Display Existing Entities
for entity in product["entities"]:

    with st.expander(f"📦 {entity['name']}"):

        st.markdown("### Add Attribute")

        with st.form(f"add_attr_{entity['name']}"):

            col1, col2 = st.columns(2)

            with col1:
                attr_name = st.text_input("Attribute Name")
                data_type = st.selectbox(
                    "Data Type",
                    ["STRING", "NUMBER", "FLOAT", "BOOLEAN", "DATE", "TIMESTAMP"]
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
                        "description": description
                    }

                    entity["attributes"].append(attribute)

                    if contains_pii:
                        product["pii"] = True

                    st.success("Attribute added.")

        st.markdown("### Current Attributes")

        if entity["attributes"]:
            for attr in entity["attributes"]:
                st.write(attr)
        else:
            st.info("No attributes yet.")
