import streamlit as st
from state_manager import initialize_state, get_progress
from components.sidebar import render_sidebar

st.set_page_config(
    page_title="GDP Data Product Steward",
    page_icon="🏛️",
    layout="wide",
)

initialize_state()
render_sidebar()

product = st.session_state.product
progress = get_progress(product)

# ── Header ──────────────────────────────────────────────────────────────
st.title("🏛️ GDP Data Product Steward")
st.caption("Governed. Structured. Production-Ready.")

# ── Dashboard Metrics ───────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Completion", f"{progress['pct']}%")
col2.metric("Entities", len(product.get("entities", [])))
col3.metric("Sources", len(product.get("sources", [])))
pii_label = "Yes" if product.get("pii") else "No"
col4.metric("PII Detected", pii_label)

st.divider()

# ── Live Canvas ─────────────────────────────────────────────────────────
if product.get("name"):
    st.subheader("📋 Live Data Product Canvas")

    left, right = st.columns(2)

    with left:
        st.markdown(f"**Product Name:** {product['name']}")
        st.markdown(f"**Domain:** {product.get('domain', '—')}")
        st.markdown(f"**Geographic Scope:** {product.get('geo_scope', '—')}")
        st.markdown(f"**Classification:** {product.get('classification') or '—'}")
        if product.get("regulatory_scope"):
            st.markdown(f"**Regulatory:** {', '.join(product['regulatory_scope'])}")

    with right:
        st.markdown(f"**Consumers:** {product.get('consumers') or '—'}")
        st.markdown(f"**Retention:** {product.get('retention_policy') or '—'}")
        st.markdown(f"**PII:** {'Yes' if product.get('pii') else 'No'}")
        if product.get("compliance_frameworks"):
            st.markdown(f"**Compliance:** {', '.join(product['compliance_frameworks'])}")

    # Entity summary
    if product.get("entities"):
        st.markdown("---")
        st.markdown("**Entities:**")
        for ent in product["entities"]:
            attr_count = len(ent.get("attributes", []))
            pii_count = sum(1 for a in ent.get("attributes", []) if a.get("pii"))
            suffix = f" ({pii_count} PII)" if pii_count else ""
            st.markdown(f"- `{ent['name']}` — {attr_count} attributes{suffix}")

    # Sources summary
    if product.get("sources"):
        st.markdown("**Sources:**")
        for src in product["sources"]:
            st.markdown(f"- `{src['name']}` — {src['type']} · {src['frequency']}")

else:
    # Getting started
    st.subheader("Getting Started")
    st.markdown(
        """
        This wizard guides you through building a **complete, governed data product definition**.
        Navigate using the sidebar pages:

        | Step | Page | What You Define |
        |------|------|-----------------|
        | 1 | **Business Context** | Purpose, domain, stakeholders, regulatory scope |
        | 2 | **Data Sources** | Source systems, ownership, SLAs, risk flags |
        | 3 | **Data Model** | Entities, attributes, data types, PII tagging |
        | 4 | **Governance & Security** | Classification, retention, compliance frameworks |
        | 5 | **Data Quality** | Completeness, accuracy, timeliness thresholds |
        | 6 | **Transformations** | Processing steps and transformation logic |
        | 7 | **Review & Export** | Validate and generate Snowflake DDL, dbt, Collibra metadata |

        👈 **Start with Business Context** from the sidebar.
        """
    )
