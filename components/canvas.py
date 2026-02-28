"""
Live Data Product Canvas — frosted glass right-side panel.
Populated with every detail the user enters across all wizard steps.
"""

import json
import streamlit as st


def _section(title: str):
    """Render a canvas section header."""
    st.markdown(
        f'<div class="cv-section">{title}</div>',
        unsafe_allow_html=True,
    )


def _field(label: str, value):
    """Render a single field row — label: value."""
    if not value:
        return
    st.markdown(
        f'<div class="cv-row">'
        f'<span class="cv-field-label">{label}</span>'
        f'<span class="cv-field-value">{value}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _empty_hint(text: str):
    """Dim hint when a section has no data yet."""
    st.markdown(
        f'<div class="cv-empty">{text}</div>',
        unsafe_allow_html=True,
    )


def render_canvas():
    """Render the live canvas — glass panel populated with user data."""
    product = st.session_state.product

    # ── Glass panel wrapper ────────────────────────────────────
    st.markdown('<div class="canvas-panel">', unsafe_allow_html=True)

    # ── Label ────────────────────────────────────────────────
    st.markdown(
        '<div class="canvas-label">[ LIVE CANVAS ]</div>',
        unsafe_allow_html=True,
    )

    name = product.get("name")

    if not name:
        st.markdown(
            '<div class="canvas-heading">Data Product Blueprint</div>'
            '<div class="cv-empty" style="margin-top:1.5rem;">'
            "Complete <b>Business Context</b> to begin populating your canvas."
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # ── Product name as main title ───────────────────────────
    st.markdown(
        f'<div class="canvas-heading">{name}</div>',
        unsafe_allow_html=True,
    )

    # ═══════════════════════════════════════════════════════════
    # 1. BUSINESS CONTEXT
    # ═══════════════════════════════════════════════════════════
    _section("Business Context")
    _field("Domain", product.get("domain"))
    _field("Geography", product.get("geo_scope"))
    _field("Objective", product.get("objective"))
    _field("Consumers", product.get("consumers"))
    if product.get("regulatory_scope"):
        _field("Regulations", " · ".join(product["regulatory_scope"]))

    # ═══════════════════════════════════════════════════════════
    # 2. DATA SOURCES
    # ═══════════════════════════════════════════════════════════
    sources = product.get("sources", [])
    _section(f"Data Sources ({len(sources)})")
    if sources:
        for src in sources:
            tags = f'{src["type"]} · {src["frequency"]}'
            if src.get("criticality") == "High":
                tags += " · HIGH"
            st.markdown(
                f'<div class="cv-source-row">'
                f'<span class="cv-source-name">{src["name"]}</span>'
                f'<span class="cv-source-tags">{tags}</span>'
                f'</div>'
                f'<div class="cv-source-owner">Owner: {src.get("owner", "—")}</div>',
                unsafe_allow_html=True,
            )
    else:
        _empty_hint("No sources registered yet")

    # ═══════════════════════════════════════════════════════════
    # 3. DATA MODEL
    # ═══════════════════════════════════════════════════════════
    entities = product.get("entities", [])
    _section(f"Data Model ({len(entities)} entities)")
    if entities:
        for ent in entities:
            attrs = ent.get("attributes", [])
            n_pii = sum(1 for a in attrs if a.get("pii"))
            pii_tag = f' · <span class="cv-pii-tag">PII:{n_pii}</span>' if n_pii else ""
            st.markdown(
                f'<div class="cv-entity-name">{ent["name"]}{pii_tag}</div>',
                unsafe_allow_html=True,
            )
            for attr in attrs:
                pii_dot = '<span class="cv-pii-dot"></span>' if attr.get("pii") else ""
                st.markdown(
                    f'<div class="cv-attr-row">'
                    f'{pii_dot}'
                    f'<span class="cv-attr-name">{attr["name"]}</span>'
                    f'<span class="cv-attr-type">{attr.get("data_type", "")}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
    else:
        _empty_hint("No entities defined yet")

    # ═══════════════════════════════════════════════════════════
    # 4. GOVERNANCE & SECURITY
    # ═══════════════════════════════════════════════════════════
    has_gov = product.get("classification") or product.get("retention_policy") or product.get("compliance_frameworks")
    _section("Governance & Security")
    if has_gov:
        _field("Classification", product.get("classification"))
        _field("Retention", product.get("retention_policy"))
        if product.get("pii"):
            st.markdown(
                '<div class="cv-row"><span class="cv-field-label">PII</span>'
                '<span class="cv-pii-tag" style="font-size:0.85rem;">Contains PII</span></div>',
                unsafe_allow_html=True,
            )
        if product.get("compliance_frameworks"):
            _field("Compliance", " · ".join(product["compliance_frameworks"]))
        _field("Access Roles", product.get("access_roles"))
        _field("Lineage", product.get("lineage_notes"))
    else:
        _empty_hint("Not configured yet")

    # ═══════════════════════════════════════════════════════════
    # 5. DATA QUALITY
    # ═══════════════════════════════════════════════════════════
    qr = product.get("quality_rules", {})
    _section("Data Quality")
    if qr.get("completeness"):
        _field("Completeness", f'{qr.get("completeness", 0)}%')
        _field("Accuracy", f'{qr.get("accuracy", 0)}%')
        _field("Timeliness", f'{qr.get("timeliness", 0)}%')
        _field("Uniqueness", f'{qr.get("uniqueness", 0)}%')
        if qr.get("custom_rules"):
            _field("Custom Rules", qr["custom_rules"])
        if qr.get("alert_channel"):
            _field("Alerts", qr["alert_channel"])
    else:
        _empty_hint("No quality thresholds set")

    # ═══════════════════════════════════════════════════════════
    # 6. TRANSFORMATIONS
    # ═══════════════════════════════════════════════════════════
    transforms = product.get("transformations", [])
    _section(f"Transformations ({len(transforms)} steps)")
    if transforms:
        for i, t in enumerate(transforms, 1):
            st.markdown(
                f'<div class="cv-transform-row">'
                f'<span class="cv-transform-num">{i}</span>'
                f'<span class="cv-transform-name">{t.get("name", "Untitled")}</span>'
                f'</div>'
                f'<div class="cv-transform-desc">{t.get("description", "")}</div>',
                unsafe_allow_html=True,
            )
    else:
        _empty_hint("No transformations defined")

    # ═══════════════════════════════════════════════════════════
    # DELIVERABLES CHECKLIST
    # ═══════════════════════════════════════════════════════════
    st.markdown('<hr class="cv-divider">', unsafe_allow_html=True)
    has_model = any(len(e.get("attributes", [])) > 0 for e in entities)
    deliverables = [
        ("Snowflake DDL", has_model),
        ("Masking Policies", product.get("pii", False) and has_model),
        ("Secure Views", bool(product.get("classification")) and has_model),
        ("dbt Models", has_model),
        ("Collibra Import", bool(name)),
        ("Documentation", bool(name)),
    ]
    ready_count = sum(1 for _, r in deliverables if r)
    _section(f"Deliverables ({ready_count}/{len(deliverables)})")
    for label, ready in deliverables:
        icon = "✅" if ready else "⬜"
        st.markdown(f"{icon} {label}")

    # ── Downloads ──────────────────────────────────────────────
    st.markdown('<hr class="cv-divider">', unsafe_allow_html=True)
    with st.expander("Download", expanded=False):
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
