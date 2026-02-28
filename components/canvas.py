"""
Live Data Product Canvas — persistent right-side panel.
Shows the evolving product definition and downloadable deliverables.
"""

import json
import streamlit as st


def render_canvas():
    """Render the live canvas in the right column of each page."""
    product = st.session_state.product

    # ── Canvas Header ───────────────────────────────────────────────
    st.markdown(
        '<div class="canvas-header">📋 Live Data Product Canvas</div>',
        unsafe_allow_html=True,
    )

    name = product.get("name")

    if not name:
        st.markdown(
            '<div class="canvas-body">Complete <b>Step 1</b> to see your '
            "data product take shape here.</div>",
            unsafe_allow_html=True,
        )
        return

    # ── Product Identity ────────────────────────────────────────────
    parts = []
    if product.get("domain"):
        parts.append(product["domain"])
    if product.get("geo_scope"):
        parts.append(product["geo_scope"])

    st.markdown(f"**{name}**")
    if parts:
        st.caption(" · ".join(parts))

    # ── Quick Stats ─────────────────────────────────────────────────
    entities = product.get("entities", [])
    sources = product.get("sources", [])

    c1, c2 = st.columns(2)
    c1.metric("Entities", len(entities))
    c2.metric("Sources", len(sources))

    # ── Entity List ─────────────────────────────────────────────────
    if entities:
        for ent in entities:
            n_attr = len(ent.get("attributes", []))
            n_pii = sum(1 for a in ent.get("attributes", []) if a.get("pii"))
            pii_tag = f" · 🔴{n_pii} PII" if n_pii else ""
            st.markdown(f"`{ent['name']}` {n_attr} attrs{pii_tag}")

    # ── Governance Snapshot ─────────────────────────────────────────
    tags = []
    if product.get("classification"):
        tags.append(f"🏷️ {product['classification']}")
    if product.get("retention_policy"):
        tags.append(f"⏱️ {product['retention_policy']}")
    if product.get("pii"):
        tags.append("🔴 PII")
    if tags:
        st.markdown(" · ".join(tags))

    if product.get("regulatory_scope"):
        st.caption("Regulatory: " + ", ".join(product["regulatory_scope"]))

    # ── Deliverables Checklist ──────────────────────────────────────
    st.divider()
    st.markdown("**📦 Deliverables**")

    has_model = any(len(e.get("attributes", [])) > 0 for e in entities)
    has_gov = bool(product.get("classification") and product.get("retention_policy"))
    has_quality = bool(product.get("quality_rules"))
    has_transforms = len(product.get("transformations", [])) > 0

    deliverables = [
        ("Snowflake DDL", has_model),
        ("Masking Policies", product.get("pii", False) and has_model),
        ("Secure Views", has_gov and has_model),
        ("dbt Models", has_model),
        ("Collibra Import", bool(name)),
        ("Documentation", bool(name)),
    ]

    for label, ready in deliverables:
        icon = "✅" if ready else "⬜"
        st.markdown(f"{icon} {label}")

    # ── Downloads (available anytime) ───────────────────────────────
    st.divider()

    with st.expander("📥 Download Now", expanded=False):
        # Documentation — always available if name exists
        from core.document_engine import DocumentEngine

        doc = DocumentEngine(product)
        st.download_button(
            "Documentation (.md)",
            data=doc.generate_markdown(),
            file_name="data_product_spec.md",
            mime="text/markdown",
            key="_cv_docs",
        )

        # DDL — available if model exists
        if has_model:
            from core.snowflake_generator import SnowflakeGenerator

            sf = SnowflakeGenerator(product)
            st.download_button(
                "Snowflake DDL (.sql)",
                data=sf.generate_ddl(),
                file_name="snowflake_ddl.sql",
                mime="text/plain",
                key="_cv_ddl",
            )

            from core.dbt_generator import DbtGenerator

            dbt = DbtGenerator(product)
            st.download_button(
                "dbt schema (.yml)",
                data=dbt.generate_schema_yaml(),
                file_name="schema.yml",
                mime="text/plain",
                key="_cv_dbt",
            )

        # Full JSON — always available
        st.download_button(
            "Full Definition (.json)",
            data=json.dumps(product, indent=2, default=str),
            file_name="data_product.json",
            mime="application/json",
            key="_cv_json",
        )
