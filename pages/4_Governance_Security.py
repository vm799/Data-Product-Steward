import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from state_manager import initialize_state, mark_step_complete
from components.layout import inject_custom_css, step_header
from components.sidebar import render_sidebar
from components.helpers import render_step_nav, render_step_complete
from config import CLASSIFICATION_OPTIONS, RETENTION_OPTIONS

initialize_state()
inject_custom_css()
render_sidebar(step=4)

render_step_nav(4)
step_header(
    4,
    "4️⃣ Governance & Security",
    "Set data classification, retention, and compliance. These directly shape the security artifacts generated.",
)

product = st.session_state.product

# ── Full-width form ─────────────────────────────────────────────────────
with st.form("governance_form"):
    c1, c2 = st.columns(2)

    with c1:
        class_options = [""] + CLASSIFICATION_OPTIONS
        class_idx = (
            class_options.index(product["classification"])
            if product.get("classification") in class_options
            else 0
        )
        classification = st.selectbox(
            "Data Classification",
            class_options,
            index=class_idx,
            format_func=lambda x: "— Select Classification —" if x == "" else x,
            help="Public = open. Internal = employees. Confidential = column masking. Restricted = secure views + RLS.",
        )

        ret_options = [""] + RETENTION_OPTIONS
        ret_idx = (
            ret_options.index(product["retention_policy"])
            if product.get("retention_policy") in ret_options
            else 0
        )
        retention_policy = st.selectbox(
            "Retention Policy",
            ret_options,
            index=ret_idx,
            format_func=lambda x: "— Select Retention —" if x == "" else x,
            help="How long data is kept before archival. Regulatory requirements may dictate minimums.",
        )

        access_roles = st.text_area(
            "Access Roles (comma-separated)",
            value=product.get("access_roles", ""),
            help="Snowflake roles that get GRANT SELECT. E.g. ANALYST_ROLE, RISK_VIEWER, DATA_ENGINEER",
        )

    with c2:
        pii_present = st.checkbox(
            "Contains PII",
            value=product.get("pii", False),
            help="Auto-detected if PII attributes were tagged in Step 3. Check manually if needed.",
        )
        compliance_frameworks = st.multiselect(
            "Compliance Frameworks",
            options=["GDPR", "CCPA", "HIPAA", "SOX", "PCI-DSS", "SOC2", "BCBS 239", "DORA", "MiFID II"],
            default=product.get("compliance_frameworks", []),
            help="Select all frameworks that apply. PII data typically requires at least GDPR or CCPA.",
        )
        lineage_notes = st.text_area(
            "Data Lineage Notes",
            value=product.get("lineage_notes", ""),
            help="Describe how data flows from source to this product. E.g. Bloomberg -> raw -> staging -> product.",
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

# ── Auto-Detection Alerts ───────────────────────────────────────
st.divider()
st.markdown("#### 🔍 Auto-Detected Policies")
st.caption("These alerts are generated dynamically from your data model and selections.")

pii_attrs = []
for ent in product.get("entities", []):
    for attr in ent.get("attributes", []):
        if attr.get("pii"):
            pii_attrs.append(f"`{ent['name']}.{attr['name']}`")

if pii_attrs:
    st.warning(f"**PII detected** in: {', '.join(pii_attrs)}")
    st.markdown("- Masking policy will be auto-generated in the Snowflake DDL")
    st.markdown("- Secure views recommended for Restricted classification")

if product.get("classification") == "Restricted":
    st.error("**Restricted** — Secure views and row-level security will be enforced in generated DDL.")
elif product.get("classification") == "Confidential":
    st.warning("**Confidential** — Column masking policies will be generated for PII attributes.")

if product.get("pii") and not product.get("compliance_frameworks"):
    st.warning("PII is present but no compliance frameworks selected. Consider adding GDPR or CCPA.")

# ── Step complete prompt ──────────────────────────────
step_done = bool(product.get("classification"))
render_step_complete(4, step_done)
