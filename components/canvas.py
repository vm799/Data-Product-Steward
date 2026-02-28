"""
Live Data Product Canvas — frosted glass right-side panel.
Shows the evolving shape of the data product as the user builds it.
"""

import json
import streamlit as st


def render_canvas():
    """Render the live canvas — glass panel with teal glow."""
    product = st.session_state.product

    # ── Glass panel wrapper ────────────────────────────────────
    st.markdown('<div class="canvas-panel">', unsafe_allow_html=True)

    # ── Label + heading ────────────────────────────────────────
    st.markdown(
        '<div class="canvas-label">[ LIVE CANVAS ]</div>'
        '<div class="canvas-heading">Data Product Blueprint</div>',
        unsafe_allow_html=True,
    )

    name = product.get("name")

    if not name:
        st.markdown(
            '<div class="canvas-explain">'
            "This panel is your live blueprint. As you fill in each step, "
            "your data product takes shape here — entities, sources, governance "
            "rules, and a checklist showing which deployment artifacts are ready "
            "to generate."
            "</div>",
            unsafe_allow_html=True,
        )

        # ── Typewriter demo — shows what a finished product looks like ──
        st.markdown(
            '<div class="typewriter-demo">'
            '<div class="typewriter-line tw-dim tw-d1">// sample output</div>'
            '<div class="typewriter-line tw-bright tw-d2">Investor_Position_Summary</div>'
            '<div class="typewriter-line tw-dim tw-d3">Domain: Risk &middot; Region: UK</div>'
            '<div class="typewriter-line tw-d4">Entities: 3 &middot; Sources: 2 &middot; PII: 4 cols</div>'
            '<div class="typewriter-line tw-dim tw-d5">Classification: Confidential &middot; Retention: 7yr</div>'
            '<div class="typewriter-line tw-check tw-d6">&check; Snowflake DDL</div>'
            '<div class="typewriter-line tw-check tw-d7">&check; dbt Models &middot; &check; Masking Policies</div>'
            '<div class="typewriter-line tw-check tw-d8 tw-cursor">&check; Collibra Import &middot; &check; Docs</div>'
            "</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="canvas-body">'
            "Complete <b>Business Context</b> to begin building yours."
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # ── Subtitle ───────────────────────────────────────────────
    st.markdown(
        '<div class="canvas-explain">'
        "Updates as you build. Each section reflects your latest inputs."
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Identity ───────────────────────────────────────────────
    parts = []
    if product.get("domain"):
        parts.append(product["domain"])
    if product.get("geo_scope"):
        parts.append(product["geo_scope"])

    st.markdown(f"**{name}**")
    if parts:
        st.caption(" · ".join(parts))

    # ── Stats ──────────────────────────────────────────────────
    entities = product.get("entities", [])
    sources = product.get("sources", [])
    c1, c2 = st.columns(2)
    c1.metric("Entities", len(entities))
    c2.metric("Sources", len(sources))

    # ── Entities ───────────────────────────────────────────────
    if entities:
        for ent in entities:
            n_attr = len(ent.get("attributes", []))
            n_pii = sum(1 for a in ent.get("attributes", []) if a.get("pii"))
            pii_tag = f" · PII:{n_pii}" if n_pii else ""
            st.markdown(f"`{ent['name']}` — {n_attr} attrs{pii_tag}")

    # ── Governance ─────────────────────────────────────────────
    tags = []
    if product.get("classification"):
        tags.append(product["classification"])
    if product.get("retention_policy"):
        tags.append(product["retention_policy"])
    if product.get("pii"):
        tags.append("PII")
    if tags:
        st.markdown(" · ".join(tags))

    if product.get("regulatory_scope"):
        st.caption("Regulatory: " + ", ".join(product["regulatory_scope"]))

    # ── Quality ────────────────────────────────────────────────
    qr = product.get("quality_rules", {})
    if qr.get("completeness"):
        st.caption(
            f"Quality: {qr.get('completeness', 0)}% complete · "
            f"{qr.get('accuracy', 0)}% accurate"
        )

    # ── Transforms ─────────────────────────────────────────────
    transforms = product.get("transformations", [])
    if transforms:
        st.caption(f"Transforms: {len(transforms)} step(s)")

    # ── Deliverables ───────────────────────────────────────────
    st.divider()
    st.markdown("**Deliverables**")
    st.caption("Check = ready to generate from your inputs so far.")

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

    st.markdown("</div>", unsafe_allow_html=True)
