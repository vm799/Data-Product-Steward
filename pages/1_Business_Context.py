import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from state_manager import initialize_state
from components.sidebar import render_sidebar

initialize_state()
render_sidebar()

st.header("1️⃣ Business Context")
st.caption("Define the purpose, ownership, and regulatory scope of your data product.")

product = st.session_state.product

# Product Name
product["name"] = st.text_input(
    "Data Product Name",
    value=product["name"],
    help="Clear, descriptive name. E.g. Investor_Position_Summary",
)

# Domain Selection
domain_options = ["HR", "Finance", "Risk", "Trading", "InfoSec", "Operations"]
product["domain"] = st.selectbox(
    "Business Domain",
    domain_options,
    index=domain_options.index(product["domain"]) if product["domain"] in domain_options else 0,
)

# Geographic Scope
geo_options = ["UK", "US", "UK & US", "Global"]
product["geo_scope"] = st.selectbox("Geographic Scope", geo_options)

# Business Objective
product["objective"] = st.text_area(
    "Business Objective",
    value=product["objective"],
    help="What decision or process does this data product enable?",
)

# Regulatory Logic (deterministic, rule-based)
regulatory = []
if product["geo_scope"] in ["UK", "UK & US", "Global"]:
    regulatory.extend(["FCA", "GDPR"])
if product["geo_scope"] in ["US", "UK & US", "Global"]:
    regulatory.append("SEC")
if product["domain"] == "Trading":
    regulatory.append("MiFID II")
if product["domain"] == "HR":
    regulatory.append("Employee Privacy Laws")
product["regulatory_scope"] = regulatory

st.subheader("Detected Regulatory Considerations")
if regulatory:
    for reg in regulatory:
        st.markdown(f"- **{reg}**")
else:
    st.info("None detected based on current selections.")

# Consumers
product["consumers"] = st.text_input(
    "Primary Consumers",
    value=product.get("consumers", ""),
    help="E.g. Risk Analysts, Portfolio Managers, HR Ops",
)

# Validation
if not product["objective"]:
    st.warning("Business Objective is required for production readiness.")
