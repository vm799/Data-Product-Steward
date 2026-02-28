import streamlit as st

st.header("1️⃣ Business Context")

product = st.session_state.product

# Product Name
product["name"] = st.text_input(
    "Data Product Name",
    value=product["name"],
    help="Clear, descriptive name. E.g. Investor_Position_Summary"
)

# Domain Selection
domain_options = ["HR", "Finance", "Risk", "Trading", "InfoSec", "Operations"]
product["domain"] = st.selectbox(
    "Business Domain",
    domain_options,
    index=domain_options.index(product["domain"]) if product["domain"] in domain_options else 0
)

# Geographic Scope
geo_options = ["UK", "US", "UK & US", "Global"]
product["geo_scope"] = st.selectbox(
    "Geographic Scope",
    geo_options
)

# Business Objective
product["objective"] = st.text_area(
    "Business Objective",
    value=product["objective"],
    help="What decision or process does this data product enable?"
)

# Regulatory Logic (Non-AI Rule Based)
regulatory = []

if product["geo_scope"] in ["UK", "UK & US", "Global"]:
    regulatory.append("FCA")
    regulatory.append("GDPR")

if product["geo_scope"] in ["US", "UK & US", "Global"]:
    regulatory.append("SEC")

if product["domain"] == "Trading":
    regulatory.append("MiFID II")

if product["domain"] == "HR":
    regulatory.append("Employee Privacy Laws")

product["regulatory_scope"] = regulatory

st.subheader("Detected Regulatory Considerations")
st.write(", ".join(regulatory) if regulatory else "None detected")

# Consumers
product["consumers"] = st.text_input(
    "Primary Consumers",
    value=product.get("consumers", ""),
    help="E.g. Risk Analysts, Portfolio Managers, HR Ops"
)

# Basic Validation Warning
if not product["objective"]:
    st.warning("⚠ Business Objective is required for production readiness.")
