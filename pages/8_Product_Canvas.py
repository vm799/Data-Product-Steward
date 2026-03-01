import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import json
from datetime import datetime
import streamlit as st
from state_manager import initialize_state, get_progress
from components.layout import inject_custom_css
from components.sidebar import render_sidebar
from components.helpers import PAGE_MAP, STEP_NAMES
from core.validation_engine import ValidationEngine
from core.scoring_engine import ScoringEngine

initialize_state()
inject_custom_css()
render_sidebar()

# ── Back navigation ────────────────────────────────────────────────
st.page_link("streamlit_app.py", label="← Back to Dashboard")

product = st.session_state.product
progress = get_progress(product)
name = product.get("name")


# ── Helpers ───────────────────────────────────────────────────────────
def _cv_section(title: str, step_num: int):
    """Section header with inline edit link to the wizard step."""
    col_t, col_e = st.columns([5, 1])
    with col_t:
        st.markdown(
            f'<div class="cv-section">{title}</div>',
            unsafe_allow_html=True,
        )
    with col_e:
        st.page_link(
            PAGE_MAP[step_num],
            label=f"Edit →",
        )


def _cv_field(label: str, value):
    if not value:
        return
    st.markdown(
        f'<div class="cv-row">'
        f'<span class="cv-field-label">{label}</span>'
        f'<span class="cv-field-value">{value}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _cv_empty(text: str):
    st.markdown(
        f'<div class="cv-empty">{text}</div>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════
# HEADER — canvas label + product name
# ═══════════════════════════════════════════════════════════════════════
st.markdown(
    '<div class="canvas-label">[ LIVE PRODUCT CANVAS ]</div>',
    unsafe_allow_html=True,
)

if name:
    st.markdown(
        f'<div class="canvas-heading">{name}</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<div class="canvas-heading">Data Product Blueprint</div>',
        unsafe_allow_html=True,
    )

st.caption(
    "Single source of truth — dynamically populated as you build. "
    "Click **Edit →** on any section to jump to that wizard step."
)

# ── Readiness metrics ─────────────────────────────────────────────────
scorer = ScoringEngine(product)
score = scorer.overall_score()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Readiness", f"{score}/100")
m2.metric("Completion", f"{progress['pct']}%")
m3.metric("Steps Done", f"{progress['done']}/{progress['total']}")
m4.metric("Entities", len(product.get("entities", [])))

st.progress(progress["pct"] / 100)


# ═══════════════════════════════════════════════════════════════════════
# DELIVERABLES CHECKLIST
# ═══════════════════════════════════════════════════════════════════════
st.divider()
entities = product.get("entities", [])
has_model = any(len(e.get("attributes", [])) > 0 for e in entities)

deliverables = [
    ("Snowflake DDL", has_model, 3),
    ("Masking Policies", product.get("pii", False) and has_model, 4),
    ("Secure Views", bool(product.get("classification")) and has_model, 4),
    ("dbt Models", has_model, 6),
    ("Collibra Import", bool(name), 7),
    ("Documentation", bool(name), 7),
]
ready_count = sum(1 for _, r, _ in deliverables if r)

st.markdown(
    f'<div class="cv-section">Deliverables ({ready_count}/{len(deliverables)})</div>',
    unsafe_allow_html=True,
)

d_cols = st.columns(3)
for i, (label, ready, _step) in enumerate(deliverables):
    with d_cols[i % 3]:
        icon = "✅" if ready else "⬜"
        st.markdown(f"{icon} {label}")

# ── Quick downloads ───────────────────────────────────────────────────
with st.expander("Download Artifacts", expanded=False):
    from core.document_engine import DocumentEngine

    doc = DocumentEngine(product)
    dl1, dl2, dl3, dl4 = st.columns(4)
    with dl1:
        st.download_button(
            "Docs (.md)",
            data=doc.generate_markdown(),
            file_name="data_product_spec.md",
            mime="text/markdown",
            key="_cvp_docs",
        )
    if has_model:
        from core.snowflake_generator import SnowflakeGenerator
        from core.dbt_generator import DbtGenerator

        sf = SnowflakeGenerator(product)
        dbt = DbtGenerator(product)
        with dl2:
            st.download_button(
                "DDL (.sql)",
                data=sf.generate_ddl(),
                file_name="snowflake_ddl.sql",
                mime="text/plain",
                key="_cvp_ddl",
            )
        with dl3:
            st.download_button(
                "dbt (.yml)",
                data=dbt.generate_schema_yaml(),
                file_name="schema.yml",
                mime="text/plain",
                key="_cvp_dbt",
            )
    with dl4:
        st.download_button(
            "JSON",
            data=json.dumps(product, indent=2, default=str),
            file_name="data_product.json",
            mime="application/json",
            key="_cvp_json",
        )


# ═══════════════════════════════════════════════════════════════════════
# SECTION 1 — BUSINESS CONTEXT
# ═══════════════════════════════════════════════════════════════════════
st.divider()
_cv_section("1. Business Context", 1)
if name:
    _cv_field("Name", name)
    _cv_field("Domain", product.get("domain"))
    _cv_field("Geography", product.get("geo_scope"))
    _cv_field("Objective", product.get("objective"))
    _cv_field("Consumers", product.get("consumers"))
    if product.get("regulatory_scope"):
        _cv_field("Regulations", " · ".join(product["regulatory_scope"]))
else:
    _cv_empty("Not started — complete Business Context to begin")


# ═══════════════════════════════════════════════════════════════════════
# SECTION 2 — DATA SOURCES
# ═══════════════════════════════════════════════════════════════════════
st.divider()
_cv_section("2. Data Sources", 2)
sources = product.get("sources", [])
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
    _cv_empty("No sources registered yet")


# ═══════════════════════════════════════════════════════════════════════
# SECTION 3 — DATA MODEL
# ═══════════════════════════════════════════════════════════════════════
st.divider()
_cv_section("3. Data Model", 3)
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
    _cv_empty("No entities defined yet")


# ═══════════════════════════════════════════════════════════════════════
# SECTION 4 — GOVERNANCE & SECURITY
# ═══════════════════════════════════════════════════════════════════════
st.divider()
_cv_section("4. Governance & Security", 4)
has_gov = (
    product.get("classification")
    or product.get("retention_policy")
    or product.get("compliance_frameworks")
)
if has_gov:
    _cv_field("Classification", product.get("classification"))
    _cv_field("Retention", product.get("retention_policy"))
    if product.get("pii"):
        st.markdown(
            '<div class="cv-row"><span class="cv-field-label">PII</span>'
            '<span class="cv-pii-tag" style="font-size:0.85rem;">Contains PII</span></div>',
            unsafe_allow_html=True,
        )
    if product.get("compliance_frameworks"):
        _cv_field("Compliance", " · ".join(product["compliance_frameworks"]))
    _cv_field("Access Roles", product.get("access_roles"))
    _cv_field("Lineage", product.get("lineage_notes"))
else:
    _cv_empty("Not configured yet")


# ═══════════════════════════════════════════════════════════════════════
# SECTION 5 — DATA QUALITY
# ═══════════════════════════════════════════════════════════════════════
st.divider()
_cv_section("5. Data Quality", 5)
qr = product.get("quality_rules", {})
if qr.get("completeness"):
    q1, q2, q3, q4 = st.columns(4)
    q1.metric("Completeness", f'{qr.get("completeness", 0)}%')
    q2.metric("Accuracy", f'{qr.get("accuracy", 0)}%')
    q3.metric("Timeliness", f'{qr.get("timeliness_hours", "—")}h')
    q4.metric("Uniqueness", f'{qr.get("uniqueness", 0)}%')
    if qr.get("custom_rules"):
        _cv_field("Custom Rules", qr["custom_rules"])
    if qr.get("monitoring_channel"):
        _cv_field("Alerts", qr["monitoring_channel"])
else:
    _cv_empty("No quality thresholds set")


# ═══════════════════════════════════════════════════════════════════════
# SECTION 6 — TRANSFORMATIONS
# ═══════════════════════════════════════════════════════════════════════
st.divider()
_cv_section("6. Transformations", 6)
transforms = product.get("transformations", [])
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
    _cv_empty("No transformations defined")


# ═══════════════════════════════════════════════════════════════════════
# VALIDATION SUMMARY
# ═══════════════════════════════════════════════════════════════════════
st.divider()
st.markdown(
    '<div class="cv-section">Validation</div>',
    unsafe_allow_html=True,
)

validator = ValidationEngine(product)
results = validator.validate()

if results["errors"]:
    for err in results["errors"]:
        st.error(err)
if results["warnings"]:
    for warn in results["warnings"]:
        st.warning(warn)
if results["valid"]:
    st.success(f"All checks passed — readiness score: {score}/100")


# ═══════════════════════════════════════════════════════════════════════
# CONTRACT SIGN-OFF
# ═══════════════════════════════════════════════════════════════════════
st.divider()
st.markdown("## Contract Sign-Off")
st.caption(
    "Approve this data product definition as the final contract. "
    "All stakeholders should review the canvas above before signing off."
)

can_sign = results["valid"] and progress["pct"] >= 85

if st.session_state.get("signed_off"):
    so = st.session_state["signed_off"]
    st.markdown(
        f'<div class="step-complete-prompt">'
        f'<div class="step-complete-prompt-title">✅ Contract Approved</div>'
        f'<div class="step-complete-prompt-desc">'
        f'Signed off by <b>{so["approver"]}</b> on {so["timestamp"]}'
        f'</div></div>',
        unsafe_allow_html=True,
    )
    st.balloons()
elif can_sign:
    approver = st.text_input(
        "Approver Name",
        help="Name of the person approving this data product contract.",
    )
    if st.button(
        "Sign Off — Approve Data Product Contract",
        use_container_width=True,
        disabled=not approver,
    ):
        st.session_state["signed_off"] = {
            "approver": approver,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "readiness_score": score,
            "completion_pct": progress["pct"],
        }
        st.rerun()
else:
    remaining = []
    if not results["valid"]:
        remaining.append(f"{len(results['errors'])} validation error(s)")
    if progress["pct"] < 85:
        remaining.append(f"completion at {progress['pct']}% (need 85%+)")
    st.warning(
        f"Cannot sign off yet — {' and '.join(remaining)}. "
        "Use the **Edit →** links above to complete each section."
    )
