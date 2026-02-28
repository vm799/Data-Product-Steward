"""
Canvas Preview Component
Shows a live summary/preview canvas of the data product being built.
"""

import streamlit as st


def render_canvas():
    """Render a live preview canvas summarizing the data product."""
    st.subheader("Canvas Preview")

    product = st.session_state.get("product", {})
    ctx = st.session_state.get("business_context", {})
    sources = st.session_state.get("data_sources", [])
    model = st.session_state.get("data_model", {})

    name = product.get("name") or ctx.get("product_name", "—")
    domain = product.get("domain") or ctx.get("domain", "—")

    st.markdown(f"**Name:** {name}")
    st.markdown(f"**Domain:** {domain}")
    st.markdown(f"**Sources:** {len(sources)}")
    st.markdown(f"**Entities:** {len(model.get('entities', []))}")
