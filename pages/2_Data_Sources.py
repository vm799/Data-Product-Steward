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
render_sidebar(step=2)

step_header(2, "2️⃣ Data Sources", "Register every source system that feeds into this data product.")
render_step_nav(2)

product = st.session_state.product

# ── Two-panel layout ────────────────────────────────────────────────────
form_col, canvas_col = st.columns([7, 3])

with form_col:
    st.markdown("#### Add a Data Source")
    st.caption("Each source needs an owner and metadata. External sources trigger governance alerts automatically.")

    with st.form("add_source_form"):
        source_name = st.text_input(
            "Source System Name",
            help="The name of the upstream system. E.g. Bloomberg, Workday, Internal Risk DB",
        )

        c1, c2 = st.columns(2)
        with c1:
            source_type = st.selectbox(
                "Source Type",
                ["Internal", "External", "Vendor"],
                help="External and Vendor sources require enhanced due diligence.",
            )
            owner = st.text_input(
                "Data Owner",
                help="The person or team accountable for this source. Required for governance.",
            )
            frequency = st.selectbox(
                "Refresh Frequency",
                ["Real-Time", "Hourly", "Daily", "Weekly", "Monthly"],
                help="How often this source delivers new data. Affects timeliness SLAs.",
            )

        with c2:
            volume = st.selectbox(
                "Estimated Volume",
                ["Low (<1GB)", "Medium (1-50GB)", "High (50-500GB)", "Very High (500GB+)"],
                help="Approximate data size per refresh. Impacts Snowflake warehouse sizing.",
            )
            structure = st.selectbox(
                "Data Structure",
                ["Structured", "Semi-Structured", "Unstructured"],
                help="Structured = relational. Semi-Structured = JSON/XML. Unstructured = files/PDFs.",
            )
            criticality = st.selectbox(
                "Business Criticality",
                ["Low", "Medium", "High"],
                help="High criticality without an SLA will trigger a governance alert.",
            )

        sla_required = st.checkbox("SLA Required?", help="Check if this source has a formal delivery SLA.")
        submitted = st.form_submit_button("Add Source")

        if submitted:
            if not source_name:
                st.error("Source Name is required.")
            elif not owner:
                st.error("Data Owner is mandatory — no orphan data allowed.")
            else:
                product["sources"].append({
                    "name": source_name,
                    "type": source_type,
                    "owner": owner,
                    "frequency": frequency,
                    "volume": volume,
                    "structure": structure,
                    "sla_required": sla_required,
                    "criticality": criticality,
                })
                st.success(f"Source **{source_name}** registered.")

    # ── Registered Sources ──────────────────────────────────────────
    if product["sources"]:
        st.divider()
        st.markdown(f"#### Registered Sources ({len(product['sources'])})")
        for i, src in enumerate(product["sources"]):
            with st.expander(f"📡 {src['name']} — {src['type']} · {src['frequency']}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"**Owner:** {src['owner']}")
                    st.markdown(f"**Frequency:** {src['frequency']}")
                    st.markdown(f"**Volume:** {src['volume']}")
                with c2:
                    st.markdown(f"**Structure:** {src['structure']}")
                    st.markdown(f"**Criticality:** {src['criticality']}")
                    st.markdown(f"**SLA:** {'Yes' if src['sla_required'] else 'No'}")
                if st.button("Remove", key=f"rm_src_{i}"):
                    product["sources"].pop(i)
                    st.rerun()

        # ── Governance Alerts ───────────────────────────────────────
        alerts = []
        for src in product["sources"]:
            if src["type"] in ["External", "Vendor"]:
                alerts.append(f"**{src['name']}:** External/Vendor source — enhanced due diligence required.")
            if src["volume"] in ["High (50-500GB)", "Very High (500GB+)"] and src["frequency"] in ["Real-Time", "Hourly"]:
                alerts.append(f"**{src['name']}:** High volume + high frequency may impact Snowflake cost.")
            if src["criticality"] == "High" and not src["sla_required"]:
                alerts.append(f"**{src['name']}:** High criticality without SLA defined.")
        if alerts:
            st.markdown("#### ⚠️ Governance Alerts")
            for alert in alerts:
                st.warning(alert)
    else:
        st.info("No sources registered yet. Add at least one source above.")

    # ── Step complete prompt ──────────────────────────────
    step_done = len(product["sources"]) > 0
    render_step_complete(2, step_done)

with canvas_col:
    render_canvas()
