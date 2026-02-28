import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from state_manager import initialize_state
from components.layout import inject_custom_css, step_header
from components.sidebar import render_sidebar
from components.canvas import render_canvas
from components.helpers import render_step_nav

initialize_state()
inject_custom_css()
render_sidebar(step=1)

step_header(1, "1️⃣ Business Context", "Define the purpose, ownership, and regulatory scope of your data product.")

product = st.session_state.product

# ── Two-panel layout: Form | Canvas ─────────────────────────────────────
form_col, canvas_col = st.columns([5, 3])

with form_col:
    product["name"] = st.text_input(
        "Data Product Name",
        value=product["name"],
        help="A clear, descriptive name. E.g. Investor_Position_Summary, Trade_Lifecycle_Events",
    )

    domain_options = ["", "HR", "Finance", "Risk", "Trading", "InfoSec", "Operations"]
    current_idx = domain_options.index(product["domain"]) if product["domain"] in domain_options else 0
    product["domain"] = st.selectbox(
        "Business Domain",
        domain_options,
        index=current_idx,
        format_func=lambda x: "— Select Domain —" if x == "" else x,
        help="The business area that owns this data product. This determines stewardship and regulatory scope.",
    )

    geo_options = ["", "UK", "US", "UK & US", "Global"]
    current_geo = geo_options.index(product["geo_scope"]) if product["geo_scope"] in geo_options else 0
    product["geo_scope"] = st.selectbox(
        "Geographic Scope",
        geo_options,
        index=current_geo,
        format_func=lambda x: "— Select Scope —" if x == "" else x,
        help="Where this data is sourced or consumed. Drives which regulations apply automatically.",
    )

    product["objective"] = st.text_area(
        "Business Objective",
        value=product["objective"],
        help="What decision or process does this data product enable? Be specific — this appears in documentation.",
    )

    # ── Auto-detected Regulatory Scope ──────────────────────────────
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

    if regulatory:
        st.markdown("**Auto-Detected Regulatory Scope:**")
        st.markdown(" · ".join(f"**{r}**" for r in regulatory))
        st.caption("Detected from your domain and geographic selections above.")
    elif product["domain"] and product["geo_scope"]:
        st.info("No specific regulations detected for this domain/geography combination.")

    product["consumers"] = st.text_input(
        "Primary Consumers",
        value=product.get("consumers", ""),
        help="Who uses this data? E.g. Risk Analysts, Portfolio Managers, HR Ops. Drives access roles in Step 4.",
    )

    # ── Validation Feedback ─────────────────────────────────────────
    st.divider()
    filled = sum(1 for f in [product["name"], product["domain"], product["objective"]] if f)
    st.progress(filled / 3)
    st.caption(f"{filled}/3 required fields complete")

    if not product["name"]:
        st.warning("**Product Name** is required to proceed.")
    if not product["domain"]:
        st.warning("**Business Domain** must be selected.")
    if not product["objective"]:
        st.warning("**Business Objective** is required for production readiness.")

with canvas_col:
    render_canvas()

render_step_nav(1)
