import streamlit as st
from state_manager import initialize_state, get_progress
from components.layout import inject_custom_css
from components.sidebar import render_sidebar
from components.canvas import render_canvas

st.set_page_config(
    page_title="GDP Data Product Steward",
    page_icon="🏛️",
    layout="wide",
)

initialize_state()
inject_custom_css()
render_sidebar()

product = st.session_state.product
progress = get_progress(product)

# ── Hero ────────────────────────────────────────────────────────────────
st.title("🏛️ GDP Data Product Steward")
st.caption("Governed. Structured. Production-Ready.")

# ── Dashboard + Canvas ──────────────────────────────────────────────────
main_col, canvas_col = st.columns([5, 3])

with main_col:
    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Completion", f"{progress['pct']}%")
    c2.metric("Entities", len(product.get("entities", [])))
    c3.metric("Sources", len(product.get("sources", [])))
    c4.metric("PII Detected", "Yes" if product.get("pii") else "No")

    st.divider()

    if product.get("name"):
        # Live summary for returning users
        st.subheader("Welcome back")
        st.markdown(
            f"You're building **{product['name']}** in the **{product.get('domain', '—')}** domain. "
            f"Continue where you left off using the sidebar navigation."
        )

        # Show what's done and what's next
        pending = [name for name, done in progress["steps"].items() if not done]
        if pending:
            st.markdown(f"**Next up:** {pending[0]}")
        else:
            st.success(
                "All steps complete — head to **Review & Export** to generate your artifacts."
            )

    else:
        # First-time guided experience
        st.subheader("Build your data product in 7 guided steps")
        st.markdown(
            "This wizard walks you through defining a **complete, governed data product** — "
            "from business context to deployment-ready Snowflake DDL, dbt models, and Collibra metadata."
        )

        st.markdown(
            """
| Step | What You'll Define | What Gets Generated |
|------|-------------------|-------------------|
| **1. Business Context** | Purpose, domain, regulatory scope | Regulatory detection, Collibra mapping |
| **2. Data Sources** | Source systems, ownership, SLAs | dbt sources, lineage docs |
| **3. Data Model** | Entities, attributes, PII tags | Snowflake DDL, dbt schema, Collibra attributes |
| **4. Governance** | Classification, retention, compliance | Masking policies, secure views, grants |
| **5. Data Quality** | Completeness, accuracy, timeliness | dbt tests, monitoring rules |
| **6. Transformations** | Processing steps, SQL logic | dbt models, transformation docs |
| **7. Review & Export** | Validate and download everything | All artifacts in one click |
            """
        )

        st.info("👈 **Start with Business Context** from the sidebar to begin.")

with canvas_col:
    render_canvas()
