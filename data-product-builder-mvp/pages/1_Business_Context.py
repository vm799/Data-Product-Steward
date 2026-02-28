"""
Step 1: Business Context
Define the purpose, domain, stakeholders, and business value of the data product.
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from state_manager import StateManager

StateManager.initialize()

st.header("Step 1: Business Context")
st.markdown("Define the business purpose and ownership of your data product.")

with st.form("business_context_form"):
    product_name = st.text_input(
        "Data Product Name",
        value=StateManager.get("business_context", {}).get("product_name", ""),
    )
    description = st.text_area(
        "Description",
        value=StateManager.get("business_context", {}).get("description", ""),
    )
    domain = st.selectbox(
        "Business Domain",
        options=["Finance", "Marketing", "Operations", "Sales", "HR", "Product", "Other"],
        index=0,
    )
    owner = st.text_input(
        "Data Product Owner",
        value=StateManager.get("business_context", {}).get("owner", ""),
    )
    stakeholders = st.text_area(
        "Key Stakeholders (comma-separated)",
        value=StateManager.get("business_context", {}).get("stakeholders", ""),
    )
    business_value = st.text_area(
        "Business Value Statement",
        value=StateManager.get("business_context", {}).get("business_value", ""),
    )
    use_cases = st.text_area(
        "Primary Use Cases (one per line)",
        value=StateManager.get("business_context", {}).get("use_cases", ""),
    )

    submitted = st.form_submit_button("Save Business Context")
    if submitted:
        StateManager.set("business_context", {
            "product_name": product_name,
            "description": description,
            "domain": domain,
            "owner": owner,
            "stakeholders": stakeholders,
            "business_value": business_value,
            "use_cases": use_cases,
        })
        StateManager.mark_step_completed("business_context")
        st.success("Business context saved.")
