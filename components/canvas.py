"""
Live Data Product Canvas — teal right-side panel.
Shows the evolving shape of the data product as the user fills in each step.
"""

import json
import streamlit as st


def render_canvas():
    """Render the live canvas in the right column of each page."""
    product = st.session_state.product

    # ── Panel wrapper — solid teal background ──────────────────
    st.markdown('<div class="canvas-panel">', unsafe_allow_html=True)

    # ── Header + explanation ────────────────────────────────────
    st.markdown(
        '<div class="canvas-header">Live Data Product Canvas</div>',
        unsafe_allow_html=True,
    )

    name = product.get("name")

    if not name:
        # Empty state — explain what this panel is and why
        st.markdown(
            '<div class="canvas-subtitle">'
            "This panel is your live blueprint. As you complete each step of "
            "the wizard, your data product takes shape here in real time — "
            "entities, sources, governance rules, and a checklist of "
            "deployment artifacts that are ready to generate.<br><br>"
            "When a deliverable shows a check mark, it means you've provided "
            "enough information for the builder to generate that artifact "
            "(DDL, masking policy, dbt model, etc.) automatically."
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="canvas-body">'
            "Complete <b>Step 1 — Business Context</b> to see your "
            "data product appear here."
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # ── Subtitle — what evolving means ─────────────────────────
    st.markdown(
        '<div class="canvas-subtitle">'
        "This updates live as you build. Each section below reflects "
        "your latest inputs across all steps."
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Product Identity ───────────────────────────────────────
    parts = []
    if product.get("domain"):
        parts.append(product["domain"])
    if product.get("geo_scope"):
        parts.append(product["geo_scope"])

    st.markdown(f"**{name}**")
    if parts:
        st.caption(" · ".join(parts))

    # ── Quick Stats ────────────────────────────────────────────
    entities = product.get("entities", [])
    sources = product.get("sources", [])

    c1, c2 = st.columns(2)
    c1.metric("Entities", len(entities))
    c2.metric("Sources", len(sources))

    # ── Entity List ────────────────────────────────────────────
    if entities:
        for ent in entities:
            n_attr = len(ent.get("attributes", []))
            n_pii = sum(1 for a in ent.get("attributes", []) if a.get("pii"))
            pii_tag = f" · 🔴 {n_pii} PII" if n_pii else ""
            st.markdown(f"`{ent['name']}` — {n_attr} attrs{pii_tag}")

    # ── Governance Snapshot ────────────────────────────────────
    tags = []
    if product.get("classification"):
        tags.append(product["classification"])
    if product.get("retention_policy"):
        tags.append(product["retention_policy"])
    if product.get("pii"):
        tags.append("PII Detected")
    if tags:
        st.markdown(" · ".join(tags))

    if product.get("regulatory_scope"):
        st.caption("Regulatory: " + ", ".join(product["regulatory_scope"]))

    # ── Quality Snapshot ───────────────────────────────────────
    qr = product.get("quality_rules", {})
    if qr.get("completeness"):
        st.caption(
            f"Quality: {qr.get('completeness', 0)}% complete · "
            f"{qr.get('accuracy', 0)}% accurate"
        )

    # ── Transformations Snapshot ───────────────────────────────
    transforms = product.get("transformations", [])
    if transforms:
        st.caption(f"Transforms: {len(transforms)} step(s) defined")

    # ── Deliverables Checklist ─────────────────────────────────
    st.divider()
    st.markdown("**Deliverables**")
    st.caption("Check marks mean enough data exists to generate that artifact.")

    has_model = any(len(e.get("attributes", [])) > 0 for e in entities)

    deliverables = [
        ("Snowflake DDL", has_model),
        ("Masking Policies", product.get("pii", False) and has_model),
        ("Secure Views", bool(product.get("classification")) and has_model),
        ("dbt Models", has_model),
        ("Collibra Import", bool(name)),
        ("Documentation", bool(name)),
    ]

    for label, ready in deliverables:
        icon = "✅" if ready else "⬜"
        st.markdown(f"{icon} {label}")

    # ── Downloads ──────────────────────────────────────────────
    st.divider()

    with st.expander("Download Now", expanded=False):
        from core.document_engine import DocumentEngine

        doc = DocumentEngine(product)
        st.download_button(
            "Documentation (.md)",
            data=doc.generate_markdown(),
            file_name="data_product_spec.md",
            mime="text/markdown",
            key="_cv_docs",
        )

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

        st.download_button(
            "Full Definition (.json)",
            data=json.dumps(product, indent=2, default=str),
            file_name="data_product.json",
            mime="application/json",
            key="_cv_json",
        )

    # Close panel wrapper
    st.markdown("</div>", unsafe_allow_html=True)
