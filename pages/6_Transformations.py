import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from state_manager import initialize_state
from components.layout import inject_custom_css, step_header
from components.sidebar import render_sidebar
from components.canvas import render_canvas

initialize_state()
inject_custom_css()
render_sidebar(step=6)

step_header(
    6,
    "6️⃣ Transformations",
    "Document the processing steps that produce your data product. This creates audit trails and dbt models.",
)

product = st.session_state.product

# ── Two-panel layout ────────────────────────────────────────────────────
form_col, canvas_col = st.columns([5, 3])

with form_col:
    st.markdown("#### Add Transformation Step")
    st.caption(
        "Each step describes one transformation in your pipeline. "
        "Reference entity names from Step 3 for lineage integrity."
    )

    # Suggest entity names if available
    entity_names = [e["name"] for e in product.get("entities", [])]

    with st.form("add_transformation_form"):
        step_name = st.text_input(
            "Step Name",
            help="Descriptive name for this transformation. E.g. 'Clean investor records', 'Aggregate positions'.",
        )

        c1, c2 = st.columns(2)
        with c1:
            step_type = st.selectbox(
                "Transformation Type",
                ["SQL", "Python", "dbt Model", "Spark", "Other"],
                help="SQL and dbt Model types will generate dbt model SQL automatically.",
            )
            source_entity = st.text_input(
                "Source Entity / Table",
                help=f"Where data comes from. Known entities: {', '.join(entity_names) if entity_names else 'none yet'}.",
            )
            target_entity = st.text_input(
                "Target Entity / Table",
                help=f"Where data goes. Known entities: {', '.join(entity_names) if entity_names else 'none yet'}.",
            )

        with c2:
            description = st.text_area(
                "Description",
                help="What this transformation does and why. Appears in generated documentation.",
            )
            logic = st.text_area(
                "Transformation Logic / SQL",
                help="The actual SQL or pseudocode. For dbt types, this becomes the model body.",
            )

        if st.form_submit_button("Add Transformation"):
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

    # ── Defined Transformations ─────────────────────────────────────
    if product["transformations"]:
        st.divider()
        st.markdown(f"#### Defined Transformations ({len(product['transformations'])})")
        for i, t in enumerate(product["transformations"]):
            with st.expander(f"⚙️ {t['name']} ({t['type']})"):
                st.markdown(f"`{t.get('source_entity', '?')}` → `{t.get('target_entity', '?')}`")
                if t.get("description"):
                    st.markdown(t["description"])
                if t.get("logic"):
                    st.code(t["logic"], language="sql")
                if st.button("Remove", key=f"rm_tx_{i}"):
                    product["transformations"].pop(i)
                    st.rerun()
    else:
        st.info("No transformations defined yet. Add your first processing step above.")

with canvas_col:
    render_canvas()
