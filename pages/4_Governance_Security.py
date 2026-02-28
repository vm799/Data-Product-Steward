import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from state_manager import initialize_state, mark_step_complete
from components.sidebar import render_sidebar
from config import CLASSIFICATION_OPTIONS, RETENTION_OPTIONS

initialize_state()
render_sidebar()

st.header("4️⃣ Governance & Security")
st.caption("Set data classification, retention policies, and compliance frameworks.")

product = st.session_state.product

with st.form("governance_form"):
    col1, col2 = st.columns(2)

    with col1:
        classification = st.selectbox(
            "Data Classification",
            CLASSIFICATION_OPTIONS,
            index=CLASSIFICATION_OPTIONS.index(product["classification"])
            if product.get("classification") in CLASSIFICATION_OPTIONS
            else 1,
        )
        retention_policy = st.selectbox(
            "Retention Policy",
            RETENTION_OPTIONS,
            index=RETENTION_OPTIONS.index(product["retention_policy"])
            if product.get("retention_policy") in RETENTION_OPTIONS
            else 3,
        )
        access_roles = st.text_area(
            "Access Roles (comma-separated)",
            value=product.get("access_roles", ""),
            help="E.g. ANALYST_ROLE, RISK_VIEWER, DATA_ENGINEER",
        )

    with col2:
        pii_present = st.checkbox(
            "Contains PII",
            value=product.get("pii", False),
            help="Auto-detected from Data Model if PII attributes exist.",
        )
        compliance_frameworks = st.multiselect(
            "Compliance Frameworks",
            options=["GDPR", "CCPA", "HIPAA", "SOX", "PCI-DSS", "SOC2", "BCBS 239", "DORA", "MiFID II"],
            default=product.get("compliance_frameworks", []),
        )
        lineage_notes = st.text_area(
            "Data Lineage Notes",
            value=product.get("lineage_notes", ""),
            help="Describe how data flows from source to this product.",
        )

    submitted = st.form_submit_button("Save Governance Settings")

    if submitted:
        product["classification"] = classification
        product["retention_policy"] = retention_policy
        product["access_roles"] = access_roles
        product["pii"] = pii_present
        product["compliance_frameworks"] = compliance_frameworks
        product["lineage_notes"] = lineage_notes
        mark_step_complete("governance")
        st.success("Governance & security settings saved.")

# Auto-detection alerts
st.divider()
st.subheader("🔍 Auto-Detected Policies")

pii_attrs = []
for ent in product.get("entities", []):
    for attr in ent.get("attributes", []):
        if attr.get("pii"):
            pii_attrs.append(f"{ent['name']}.{attr['name']}")

if pii_attrs:
    st.warning(f"**PII detected** in: {', '.join(pii_attrs)}")
    st.markdown("- Masking policy will be auto-generated in Snowflake DDL")
    st.markdown("- Secure views recommended for Restricted classification")

if product.get("classification") == "Restricted":
    st.error("**Restricted classification** — Secure views and row-level security will be enforced.")
elif product.get("classification") == "Confidential":
    st.warning("**Confidential classification** — Column masking policies recommended.")

if product.get("pii") and not product.get("compliance_frameworks"):
    st.warning("PII is present but no compliance frameworks selected. Consider adding GDPR or CCPA.")
