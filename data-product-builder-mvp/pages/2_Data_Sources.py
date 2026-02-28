import streamlit as st

st.header("2️⃣ Data Sources")

product = st.session_state.product

if "sources" not in product:
    product["sources"] = []

st.subheader("Add Data Source")

with st.form("add_source_form"):

    source_name = st.text_input("Source System Name")

    source_type = st.selectbox(
        "Source Type",
        ["Internal", "External", "Vendor"]
    )

    owner = st.text_input("Data Owner (Required)")

    frequency = st.selectbox(
        "Refresh Frequency",
        ["Real-Time", "Hourly", "Daily", "Weekly", "Monthly"]
    )

    volume = st.selectbox(
        "Estimated Volume",
        ["Low (<1GB)", "Medium (1-50GB)", "High (50-500GB)", "Very High (500GB+)"]
    )

    structure = st.selectbox(
        "Data Structure",
        ["Structured", "Semi-Structured", "Unstructured"]
    )

    sla_required = st.checkbox("SLA Required?")

    criticality = st.selectbox(
        "Business Criticality",
        ["Low", "Medium", "High"]
    )

    submitted = st.form_submit_button("Add Source")

    if submitted:
        if not source_name:
            st.error("Source Name is required.")
        elif not owner:
            st.error("Data Owner is mandatory.")
        else:
            source = {
                "name": source_name,
                "type": source_type,
                "owner": owner,
                "frequency": frequency,
                "volume": volume,
                "structure": structure,
                "sla_required": sla_required,
                "criticality": criticality
            }

            product["sources"].append(source)
            st.success("Source added successfully.")

# Display Existing Sources
st.subheader("Current Sources")

if product["sources"]:
    for i, src in enumerate(product["sources"]):
        with st.expander(f"{src['name']}"):
            st.write(src)
else:
    st.info("No sources added yet.")

# Risk Warnings
st.subheader("Governance Alerts")

for src in product["sources"]:
    if src["type"] in ["External", "Vendor"]:
        st.warning(f"{src['name']}: External/Vendor source requires enhanced due diligence.")

    if src["volume"] in ["High (50-500GB)", "Very High (500GB+)"] and src["frequency"] in ["Real-Time", "Hourly"]:
        st.warning(f"{src['name']}: High volume + high frequency may impact Snowflake cost.")

    if src["criticality"] == "High" and not src["sla_required"]:
        st.warning(f"{src['name']}: High criticality without SLA defined.")
