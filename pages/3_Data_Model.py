import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from state_manager import initialize_state
from components.layout import inject_custom_css, step_header
from components.sidebar import render_sidebar
from components.canvas import render_canvas
from components.helpers import render_step_nav, render_step_complete

initialize_state()
inject_custom_css()
render_sidebar(step=3)

step_header(3, "3️⃣ Data Model", "Design entities (tables) and their attributes (columns) with PII classification.")
render_step_nav(3)

product = st.session_state.product

# ── Two-panel layout ────────────────────────────────────────────────────
form_col, canvas_col = st.columns([7, 3])

with form_col:
    st.markdown("#### Create Entity")
    st.caption("An entity is a table in your data product. E.g. INVESTOR, POSITION, TRADE.")

    entity_name = st.text_input(
        "Entity Name",
        help="Will be auto-uppercased to match Snowflake convention.",
    )
    if st.button("Add Entity"):
        if not entity_name:
            st.error("Entity name is required.")
        else:
            product["entities"].append({"name": entity_name.upper(), "attributes": []})
            st.success(f"Entity **{entity_name.upper()}** created. Add attributes below.")

    st.divider()

    # ── Entity Panels ───────────────────────────────────────────────
    if product["entities"]:
        for idx, entity in enumerate(product["entities"]):
            n_attr = len(entity["attributes"])
            n_pii = sum(1 for a in entity["attributes"] if a.get("pii"))
            pii_tag = f" · 🔴 {n_pii} PII" if n_pii else ""

            with st.expander(
                f"📦 {entity['name']} — {n_attr} attributes{pii_tag}",
                expanded=(n_attr == 0),
            ):
                st.markdown("**Add Attribute**")
                st.caption(
                    "Each attribute becomes a column in the generated DDL. "
                    "Marking PII auto-generates masking policies."
                )

                with st.form(f"attr_form_{idx}"):
                    c1, c2 = st.columns(2)
                    with c1:
                        attr_name = st.text_input("Attribute Name", help="Auto-uppercased.")
                        data_type = st.selectbox(
                            "Data Type",
                            ["STRING", "NUMBER", "FLOAT", "BOOLEAN", "DATE", "TIMESTAMP"],
                            help="STRING = VARCHAR, NUMBER = INTEGER, FLOAT = DECIMAL.",
                        )
                        nullable = st.checkbox("Nullable?", value=True, help="Uncheck for required fields (NOT NULL).")
                    with c2:
                        contains_pii = st.checkbox(
                            "Contains PII?",
                            help="Personal data (names, emails, SSNs, addresses). Triggers masking policy.",
                        )
                        description = st.text_input(
                            "Description",
                            help="Becomes a COMMENT on the column in Snowflake DDL.",
                        )

                    if st.form_submit_button("Add Attribute"):
                        if not attr_name:
                            st.error("Attribute name is required.")
                        else:
                            entity["attributes"].append({
                                "name": attr_name.upper(),
                                "data_type": data_type,
                                "nullable": nullable,
                                "pii": contains_pii,
                                "description": description,
                            })
                            if contains_pii:
                                product["pii"] = True
                            st.success(f"Attribute **{attr_name.upper()}** added to {entity['name']}.")

                # ── Attribute List ──────────────────────────────────
                if entity["attributes"]:
                    st.markdown("**Current Attributes:**")
                    for attr in entity["attributes"]:
                        pii_badge = " 🔴 PII" if attr.get("pii") else ""
                        null_badge = "NULL" if attr.get("nullable") else "NOT NULL"
                        desc = f" — _{attr['description']}_" if attr.get("description") else ""
                        st.markdown(f"- `{attr['name']}` · {attr['data_type']} · {null_badge}{pii_badge}{desc}")
                else:
                    st.info("No attributes yet — add at least one above.")

                if st.button("Remove Entity", key=f"rm_ent_{idx}"):
                    product["entities"].pop(idx)
                    st.rerun()
    else:
        st.info("No entities yet. Create your first entity above to start building the data model.")

    # ── Step complete prompt ──────────────────────────────
    step_done = any(len(e.get("attributes", [])) > 0 for e in product.get("entities", []))
    render_step_complete(3, step_done)

with canvas_col:
    render_canvas()
