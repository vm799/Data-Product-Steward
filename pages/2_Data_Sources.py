import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from state_manager import initialize_state
from components.sidebar import render_sidebar

initialize_state()
render_sidebar()

st.header("2️⃣ Data Sources")
st.caption("Register source systems with ownership, SLA, and risk metadata.")

product = st.session_state.product

if "sources" not in product:
    product["sources"] = []

st.subheader("Add Data Source")

with st.form("add_source_form"):
    source_name = st.text_input("Source System Name")

    col1, col2 = st.columns(2)

    with col1:
        source_type = st.selectbox("Source Type", ["Internal", "External", "Vendor"])
        owner = st.text_input("Data Owner (Required)")
        frequency = st.selectbox(
            "Refresh Frequency",
            ["Real-Time", "Hourly", "Daily", "Weekly", "Monthly"],
        )

    with col2:
        volume = st.selectbox(
            "Estimated Volume",
            ["Low (<1GB)", "Medium (1-50GB)", "High (50-500GB)", "Very High (500GB+)"],
        )
        structure = st.selectbox(
            "Data Structure",
            ["Structured", "Semi-Structured", "Unstructured"],
        )
        criticality = st.selectbox("Business Criticality", ["Low", "Medium", "High"])

    sla_required = st.checkbox("SLA Required?")

    submitted = st.form_submit_button("Add Source")

    if submitted:
        if not source_name:
            st.error("Source Name is required.")
        elif not owner:
            st.error("Data Owner is mandatory.")
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
            st.success(f"Source **{source_name}** added.")

# Display Existing Sources
st.subheader("Registered Sources")

if product["sources"]:
    for i, src in enumerate(product["sources"]):
        with st.expander(f"📡 {src['name']}"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**Type:** {src['type']}")
                st.markdown(f"**Owner:** {src['owner']}")
                st.markdown(f"**Frequency:** {src['frequency']}")
            with c2:
                st.markdown(f"**Volume:** {src['volume']}")
                st.markdown(f"**Structure:** {src['structure']}")
                st.markdown(f"**Criticality:** {src['criticality']}")
                st.markdown(f"**SLA:** {'Yes' if src['sla_required'] else 'No'}")

            if st.button(f"Remove", key=f"rm_src_{i}"):
                product["sources"].pop(i)
                st.rerun()
else:
    st.info("No sources added yet.")

# Governance Alerts
if product["sources"]:
    alerts = []
    for src in product["sources"]:
        if src["type"] in ["External", "Vendor"]:
            alerts.append(f"**{src['name']}:** External/Vendor source requires enhanced due diligence.")
        if src["volume"] in ["High (50-500GB)", "Very High (500GB+)"] and src["frequency"] in ["Real-Time", "Hourly"]:
            alerts.append(f"**{src['name']}:** High volume + high frequency may impact Snowflake cost.")
        if src["criticality"] == "High" and not src["sla_required"]:
            alerts.append(f"**{src['name']}:** High criticality without SLA defined.")

    if alerts:
        st.subheader("⚠️ Governance Alerts")
        for alert in alerts:
            st.warning(alert)
