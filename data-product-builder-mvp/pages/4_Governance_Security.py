"""
Step 4: Governance & Security
Apply governance policies, data classification, and access controls.
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from state_manager import StateManager

StateManager.initialize()

st.header("Step 4: Governance & Security")
st.markdown("Define governance policies, classification, and access controls.")

gov = StateManager.get("governance_security", {})

with st.form("governance_form"):
    data_classification = st.selectbox(
        "Data Classification",
        options=["Public", "Internal", "Confidential", "Restricted"],
        index=["Public", "Internal", "Confidential", "Restricted"].index(
            gov.get("data_classification", "Internal")
        ),
    )
    pii_present = st.checkbox("Contains PII", value=gov.get("pii_present", False))
    retention_policy = st.selectbox(
        "Retention Policy",
        options=["30 days", "90 days", "1 year", "3 years", "7 years", "Indefinite"],
    )
    access_roles = st.text_area(
        "Access Roles (comma-separated)",
        value=gov.get("access_roles", ""),
    )
    compliance_frameworks = st.multiselect(
        "Compliance Frameworks",
        options=["GDPR", "CCPA", "HIPAA", "SOX", "PCI-DSS", "SOC2"],
        default=gov.get("compliance_frameworks", []),
    )
    lineage_notes = st.text_area(
        "Data Lineage Notes",
        value=gov.get("lineage_notes", ""),
    )

    submitted = st.form_submit_button("Save Governance Settings")
    if submitted:
        StateManager.set("governance_security", {
            "data_classification": data_classification,
            "pii_present": pii_present,
            "retention_policy": retention_policy,
            "access_roles": access_roles,
            "compliance_frameworks": compliance_frameworks,
            "lineage_notes": lineage_notes,
        })
        StateManager.mark_step_completed("governance_security")
        st.success("Governance & security settings saved.")
