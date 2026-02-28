import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import json
import streamlit as st
from state_manager import initialize_state, mark_step_complete, get_progress
from components.layout import inject_custom_css, step_header
from components.sidebar import render_sidebar
from components.helpers import render_step_nav
from core.validation_engine import ValidationEngine
from core.scoring_engine import ScoringEngine
from core.snowflake_generator import SnowflakeGenerator
from core.dbt_generator import DbtGenerator
from core.collibra_generator import CollibraGenerator
from core.document_engine import DocumentEngine

initialize_state()
inject_custom_css()
render_sidebar(step=7)

render_step_nav(7)
step_header(
    7,
    "7️⃣ Review & Export",
    "Validate your data product definition and generate deployment-ready artifacts.",
)

product = st.session_state.product
progress = get_progress(product)

# ── Readiness Score ─────────────────────────────────────────────────────
scorer = ScoringEngine(product)
score = scorer.overall_score()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Readiness", f"{score}/100")
c2.metric("Completion", f"{progress['pct']}%")
c3.metric("Entities", len(product.get("entities", [])))
c4.metric("Sources", len(product.get("sources", [])))

st.progress(score / 100)

# ── Validation ──────────────────────────────────────────────────────────
st.divider()
st.subheader("🔍 Validation Results")

validator = ValidationEngine(product)
results = validator.validate()

if results["valid"]:
    st.success(f"All validation checks passed. Readiness score: {results['score']}/100")
else:
    st.error(f"Validation found {len(results['errors'])} error(s). Fix these before exporting.")

if results["errors"]:
    for err in results["errors"]:
        st.error(f"{err}")

if results["warnings"]:
    for warn in results["warnings"]:
        st.warning(f"{warn}")

# ── Step Completion ─────────────────────────────────────────────────────
st.divider()
st.subheader("📋 Step Completion")

for step_name, done in progress["steps"].items():
    icon = "✅" if done else "❌"
    st.markdown(f"{icon} {step_name}")

# ── Full Product JSON ───────────────────────────────────────────────────
with st.expander("View Full Product Definition (JSON)"):
    st.json(product)

# ── Generated Artifacts ─────────────────────────────────────────────────
st.divider()
st.subheader("🚀 Generated Artifacts")
st.caption("Each tab shows a preview of the generated artifact with a download button.")

tab_ddl, tab_mask, tab_dbt, tab_collibra, tab_docs = st.tabs([
    "Snowflake DDL",
    "Masking & Security",
    "dbt Models",
    "Collibra Metadata",
    "Documentation",
])

sf = SnowflakeGenerator(product)
dbt = DbtGenerator(product)
collibra = CollibraGenerator(product)
doc = DocumentEngine(product)

with tab_ddl:
    ddl = sf.generate_ddl()
    st.code(ddl, language="sql")
    st.download_button("Download DDL", data=ddl, file_name="snowflake_ddl.sql", mime="text/plain")

    grants = sf.generate_grants()
    if grants and "No access roles" not in grants:
        st.markdown("#### Access Grants")
        st.code(grants, language="sql")

with tab_mask:
    masking = sf.generate_masking_policies()
    st.code(masking, language="sql")

    views = sf.generate_secure_views()
    st.markdown("#### Secure Views")
    st.code(views, language="sql")

    st.download_button(
        "Download Security Policies",
        data=masking + "\n\n" + views,
        file_name="snowflake_security.sql",
        mime="text/plain",
    )

with tab_dbt:
    schema_yaml = dbt.generate_schema_yaml()
    st.markdown("#### schema.yml")
    st.code(schema_yaml, language="yaml")

    models = dbt.generate_all_models()
    for filename, sql in models.items():
        st.markdown(f"#### {filename}")
        st.code(sql, language="sql")

    st.download_button("Download schema.yml", data=schema_yaml, file_name="schema.yml", mime="text/plain")

with tab_collibra:
    collibra_json = collibra.to_json()
    st.code(collibra_json, language="json")
    st.download_button(
        "Download Collibra Import",
        data=collibra_json,
        file_name="collibra_import.json",
        mime="application/json",
    )

with tab_docs:
    markdown = doc.generate_markdown()
    st.markdown(markdown)
    st.download_button(
        "Download Documentation",
        data=markdown,
        file_name="data_product_spec.md",
        mime="text/markdown",
    )

# ── Full Export ─────────────────────────────────────────────────────────
st.divider()
st.subheader("📦 Full Export")

full_json = json.dumps(product, indent=2, default=str)
st.download_button(
    "Download Complete Definition (JSON)",
    data=full_json,
    file_name="data_product_definition.json",
    mime="application/json",
)

if results["valid"] and progress["pct"] >= 85:
    mark_step_complete("review")
    st.success("Data product definition is complete and ready for deployment.")
    st.balloons()
