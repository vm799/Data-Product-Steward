import streamlit as st
from state_manager import initialize_state, get_progress
from components.layout import inject_custom_css
from components.sidebar import render_sidebar
from components.canvas import render_canvas

st.set_page_config(
    page_title="Data Product Builder — Asset Management",
    page_icon="📊",
    layout="wide",
)

initialize_state()
inject_custom_css()
render_sidebar()

product = st.session_state.product
progress = get_progress(product)

# ═══════════════════════════════════════════════════════════════════════
# HEADER — clear branding, no jargon
# ═══════════════════════════════════════════════════════════════════════
st.markdown(
    '<div class="dashboard-hero">'
    "<h1>📊 Data Product Builder</h1>"
    "<p>Build production-ready, governed data products for asset management — "
    "step by step, no experience required.</p>"
    "</div>",
    unsafe_allow_html=True,
)

# ═══════════════════════════════════════════════════════════════════════
# RETURNING USER — show progress summary at the top
# ═══════════════════════════════════════════════════════════════════════
if product.get("name"):
    st.markdown("---")
    rc1, rc2, rc3, rc4 = st.columns(4)
    rc1.metric("Building", product["name"])
    rc2.metric("Progress", f"{progress['pct']}%")
    rc3.metric("Entities", len(product.get("entities", [])))
    rc4.metric("Sources", len(product.get("sources", [])))

    pending = [name for name, done in progress["steps"].items() if not done]
    if pending:
        st.info(
            f"**Welcome back.** You're working on **{product['name']}** "
            f"in the **{product.get('domain', '—')}** domain. "
            f"Your next step: **{pending[0]}** — select it from the sidebar."
        )
    else:
        st.success(
            "**All steps complete.** Head to **Review & Export** in the sidebar "
            "to validate and download your production artifacts."
        )

# ═══════════════════════════════════════════════════════════════════════
# ONBOARDING — always visible so any new user can orient themselves
# ═══════════════════════════════════════════════════════════════════════

main_col, canvas_col = st.columns([5, 3])

with main_col:

    # ── What is this tool? ──────────────────────────────────────────
    st.markdown(
        '<div class="onboard-section">'
        "<h3>What is this?</h3>"
        "<p>In asset management, a <b>Data Product</b> is a curated, governed dataset "
        "built for a specific business purpose — like an Investor Position Summary or a "
        "Risk Exposure Report. Before data reaches dashboards or models, it needs "
        "structure, ownership, security rules, quality checks, and compliance metadata.</p>"
        "<p>This builder walks you through <b>every decision</b> required to take a data "
        "product from idea to production-ready deployment — including Snowflake DDL, "
        "dbt transformation models, masking policies, and Collibra governance metadata. "
        "No prior data engineering experience required.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    # ── How does the screen work? ───────────────────────────────────
    st.markdown(
        '<div class="onboard-section">'
        "<h3>How this screen is laid out</h3>"
        "</div>",
        unsafe_allow_html=True,
    )

    z1, z2, z3 = st.columns(3)
    with z1:
        st.markdown(
            '<div class="zone-card zone-sidebar">'
            '<div class="zone-label">◀ LEFT SIDEBAR</div>'
            "<b>Navigation & Help</b><br>"
            "Your progress tracker, step-by-step checklist, "
            "contextual tips for each step, and a glossary of key terms. "
            "Click any page name in the sidebar to jump to that step."
            "</div>",
            unsafe_allow_html=True,
        )
    with z2:
        st.markdown(
            '<div class="zone-card zone-wizard">'
            '<div class="zone-label">CENTER</div>'
            "<b>The Wizard (you are here)</b><br>"
            "Each step opens a form in the center. Fill it in, "
            "save, and move to the next step. The wizard guides you "
            "through everything — business context, data model, "
            "governance, quality rules, and transformations."
            "</div>",
            unsafe_allow_html=True,
        )
    with z3:
        st.markdown(
            '<div class="zone-card zone-canvas">'
            '<div class="zone-label">RIGHT PANEL ▶</div>'
            "<b>Live Data Product Canvas</b><br>"
            "As you fill in each step, the canvas on the right updates "
            "in real time — showing your entities, sources, governance "
            "status, and a checklist of deliverables that are ready to "
            "generate. Think of it as your live blueprint."
            "</div>",
            unsafe_allow_html=True,
        )

    # ── The 7-Step Journey ──────────────────────────────────────────
    st.markdown(
        '<div class="onboard-section">'
        "<h3>Your 7-step journey</h3>"
        "<p>Each step builds on the last. Complete them in order for best results. "
        "You can always go back and edit earlier steps.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    steps_data = [
        {
            "num": "1",
            "name": "Business Context",
            "what": "Name your data product, pick the business domain (e.g. Risk, Trading, HR), "
            "set the geographic scope, and describe the business objective.",
            "why": "This determines which regulations apply automatically (FCA, GDPR, SEC, MiFID II) "
            "and who consumes the data. Everything else flows from this.",
            "produces": "Regulatory scope, Collibra domain mapping",
        },
        {
            "num": "2",
            "name": "Data Sources",
            "what": "Register every upstream system that feeds into your data product — "
            "name it, assign an owner, set refresh frequency and criticality.",
            "why": "In asset management, data without a named owner is a compliance risk. "
            "This step ensures every source is accountable and SLA-tracked.",
            "produces": "dbt source definitions, lineage documentation",
        },
        {
            "num": "3",
            "name": "Data Model",
            "what": "Design your entities (tables) and their attributes (columns). "
            "Set data types, mark which columns contain PII (personal data).",
            "why": "This is the backbone. Tagging a column as PII here automatically generates "
            "Snowflake masking policies — one checkbox, full security.",
            "produces": "Snowflake DDL, dbt schema, Collibra attributes",
        },
        {
            "num": "4",
            "name": "Governance & Security",
            "what": "Classify sensitivity (Public → Restricted), set retention periods, "
            "assign access roles, and select compliance frameworks.",
            "why": "'Restricted' data gets secure views + row-level security. "
            "'Confidential' gets column masking. This isn't optional — regulators audit it.",
            "produces": "Masking policies, secure views, access grants",
        },
        {
            "num": "5",
            "name": "Data Quality",
            "what": "Set thresholds for completeness, accuracy, timeliness, and uniqueness. "
            "Add custom quality rules and an alerting channel.",
            "why": "Quality thresholds become automated pipeline checks. "
            "If completeness drops below 95%, alerts fire before bad data reaches production.",
            "produces": "dbt tests, monitoring rules, quality documentation",
        },
        {
            "num": "6",
            "name": "Transformations",
            "what": "Document each processing step — source table, target table, "
            "transformation type (SQL, dbt, Python), and the logic.",
            "why": "Regulators require lineage — proof of how data was transformed. "
            "This step creates that audit trail and generates runnable dbt models.",
            "produces": "dbt model SQL, transformation docs, lineage map",
        },
        {
            "num": "7",
            "name": "Review & Export",
            "what": "Validate your definition, check the readiness scorecard, "
            "fix any errors, and download all production artifacts.",
            "why": "This is your quality gate. Nothing ships until the validator confirms "
            "your data product is complete, consistent, and production-worthy.",
            "produces": "Snowflake DDL, dbt models, Collibra import, full docs",
        },
    ]

    for s in steps_data:
        done = list(progress["steps"].values())[int(s["num"]) - 1]
        status_icon = "✅" if done else f"Step {s['num']}"
        status_cls = "step-done" if done else "step-pending"

        st.markdown(
            f'<div class="journey-step">'
            f'<div class="journey-step-badge {status_cls}">{status_icon}</div>'
            f'<div class="journey-step-body">'
            f'<div class="journey-step-title">{s["name"]}</div>'
            f'<div class="journey-step-what"><b>What you do:</b> {s["what"]}</div>'
            f'<div class="journey-step-why"><b>Why it matters:</b> {s["why"]}</div>'
            f'<div class="journey-step-produces">Generates → {s["produces"]}</div>'
            f"</div></div>",
            unsafe_allow_html=True,
        )

    # ── What you'll get at the end ──────────────────────────────────
    st.markdown(
        '<div class="onboard-section">'
        "<h3>What you get at the end</h3>"
        "<p>After completing all 7 steps, you can download a full suite of "
        "<b>production-ready artifacts</b> with one click:</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown(
            '<div class="deliverable-card">'
            "<b>Snowflake Package</b><br>"
            "DDL to create tables, masking policies for PII columns, "
            "secure views for restricted data, GRANT statements for access roles."
            "</div>",
            unsafe_allow_html=True,
        )
    with d2:
        st.markdown(
            '<div class="deliverable-card">'
            "<b>dbt Package</b><br>"
            "schema.yml with tests and docs, source definitions, "
            "transformation models with SQL logic, ready to run."
            "</div>",
            unsafe_allow_html=True,
        )
    with d3:
        st.markdown(
            '<div class="deliverable-card">'
            "<b>Governance Package</b><br>"
            "Collibra import JSON for metadata catalog, full Markdown "
            "documentation, and a complete JSON definition for version control."
            "</div>",
            unsafe_allow_html=True,
        )

    # ── Call to action ──────────────────────────────────────────────
    st.markdown("---")
    st.markdown(
        '<div class="cta-box">'
        "👈 <b>Open the sidebar</b> and click <b>Business Context</b> to start building "
        "your first data product. The canvas on the right will update as you go."
        "</div>",
        unsafe_allow_html=True,
    )

with canvas_col:
    render_canvas()
