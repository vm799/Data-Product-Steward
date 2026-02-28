"""
Per-step contextual guidance shown in the sidebar.
Each step has: why it matters (in plain English), practical tips, and what it feeds into.
Written for someone with zero data engineering experience.
"""

import streamlit as st

# ── Page file paths for navigation ─────────────────────────────────────
PAGE_MAP = {
    1: "pages/1_Business_Context.py",
    2: "pages/2_Data_Sources.py",
    3: "pages/3_Data_Model.py",
    4: "pages/4_Governance_Security.py",
    5: "pages/5_Data_Quality.py",
    6: "pages/6_Transformations.py",
    7: "pages/7_Review_Export.py",
}

STEP_NAMES = [
    "Business Context",
    "Data Sources",
    "Data Model",
    "Governance & Security",
    "Data Quality",
    "Transformations",
    "Review & Export",
]


def render_step_nav(current_step: int):
    """Render prev / dashboard / next navigation footer at bottom of a wizard page."""
    st.divider()
    prev_col, dash_col, next_col = st.columns(3)

    with prev_col:
        if current_step > 1:
            st.page_link(
                PAGE_MAP[current_step - 1],
                label=f"← {STEP_NAMES[current_step - 2]}",
            )
        else:
            st.page_link("streamlit_app.py", label="← Dashboard")

    with dash_col:
        st.page_link("streamlit_app.py", label="⌂ Dashboard")

    with next_col:
        if current_step < 7:
            st.page_link(
                PAGE_MAP[current_step + 1],
                label=f"{STEP_NAMES[current_step]} →",
            )
        else:
            st.page_link("streamlit_app.py", label="⌂ Dashboard")

STEP_GUIDES = {
    1: {
        "title": "Business Context — Why?",
        "why": (
            "Every data product starts with <b>who needs it</b> and <b>what it's for</b>. "
            "Defining your business domain and geographic scope here lets the tool "
            "<b>automatically detect which regulations apply</b> — e.g. UK data triggers "
            "FCA and GDPR rules; Trading data triggers MiFID II. You won't need to "
            "look these up yourself."
        ),
        "tips": [
            "Pick a descriptive name like `Investor_Position_Summary` — this becomes the title everywhere",
            "Regulatory scope is auto-detected: just pick domain + geography and we handle the rest",
            "Be specific about consumers (who reads this data?) — it drives access roles later",
            "The 'Business Objective' should be one clear sentence: what decision does this data support?",
        ],
        "feeds": "Regulatory detection, Collibra domain mapping, document header",
    },
    2: {
        "title": "Data Sources — Why?",
        "why": (
            "Before you build anything, you need to document <b>where the data comes from</b>. "
            "In asset management, data without a named owner is a compliance risk. "
            "This step ensures every source system has <b>accountability, an SLA, and a "
            "criticality rating</b>. The tool will flag risks automatically — like external "
            "sources needing extra due diligence."
        ),
        "tips": [
            "Every source MUST have a named Data Owner — regulators check for this",
            "High-criticality sources without SLAs get flagged as governance alerts",
            "External or vendor data triggers 'enhanced due diligence' warnings",
            "Volume + frequency impacts cost — the tool warns you about expensive combos",
        ],
        "feeds": "dbt source definitions, lineage documentation, risk assessment",
    },
    3: {
        "title": "Data Model — Why?",
        "why": (
            "This is the backbone of your data product: the <b>tables (entities) and "
            "columns (attributes)</b> that define its structure. The critical action here "
            "is <b>PII tagging</b> — checking 'Contains PII' on a column automatically "
            "creates a Snowflake masking policy that hides that value from unauthorized "
            "users. One checkbox = complete security policy."
        ),
        "tips": [
            "Names are auto-uppercased to match Snowflake naming convention",
            "Tag EVERY column containing personal data as PII — this generates masking policies",
            "Descriptions become SQL COMMENTs in the generated DDL — worth filling in",
            "You can add multiple entities (tables) — each with its own set of columns",
        ],
        "feeds": "Snowflake DDL, dbt schema.yml, Collibra attributes, masking policies",
    },
    4: {
        "title": "Governance & Security — Why?",
        "why": (
            "Classification determines what <b>security controls get generated</b>: "
            "<b>Restricted</b> data gets secure views + row-level security. "
            "<b>Confidential</b> data gets column masking. This isn't a label — it directly "
            "controls what code is produced. Regulators audit these controls, so getting "
            "this right is non-negotiable."
        ),
        "tips": [
            "If PII columns exist (from Step 3), add at least GDPR or CCPA to compliance",
            "Restricted = strongest tier — use for MNPI (material non-public info) and PII",
            "Access roles map directly to Snowflake GRANT statements (e.g. ANALYST_ROLE, RISK_ROLE)",
            "Retention period: regulated firms typically need 3–7 years minimum",
        ],
        "feeds": "Masking policies, secure views, access grants, compliance metadata",
    },
    5: {
        "title": "Data Quality — Why?",
        "why": (
            "Quality thresholds define what <b>'good enough' means</b> for your data product. "
            "These become <b>automated pipeline checks</b> — if completeness drops below "
            "your threshold, alerts fire to your Slack or email before bad data reaches "
            "dashboards or trading models. 95% completeness is the industry baseline."
        ),
        "tips": [
            "95% completeness is standard — adjust up or down based on how critical the data is",
            "Timeliness should match the SLAs you set in Step 2 (e.g. daily source → 24h SLA)",
            "Custom rules become dbt tests — write things like 'amount > 0' or 'currency IN (USD, GBP)'",
            "Set an alerting channel so quality failures notify the right people",
        ],
        "feeds": "dbt tests, monitoring rules, quality documentation",
    },
    6: {
        "title": "Transformations — Why?",
        "why": (
            "Transformation steps document <b>how raw data becomes the final product</b>. "
            "This creates an <b>audit trail</b> that regulators require — proof of every "
            "change applied to the data. The SQL you write here becomes runnable "
            "dbt models that your data engineering team can deploy immediately."
        ),
        "tips": [
            "Reference entity names from Step 3 — the tool suggests them for consistency",
            "Chain transforms: raw source → staging (clean) → final (business-ready)",
            "SQL logic becomes the body of generated dbt models — write production SQL",
            "Every step should have a clear description explaining the business logic",
        ],
        "feeds": "dbt model SQL, transformation docs, lineage mapping",
    },
    7: {
        "title": "Review & Export — Your Quality Gate",
        "why": (
            "This is the <b>final checkpoint</b> before generating production artifacts. "
            "The validator checks that your data product definition is <b>complete and "
            "consistent</b> — e.g. PII columns exist but no compliance framework is set? "
            "That's an error. Fix all errors, then download everything."
        ),
        "tips": [
            "Fix all red errors before exporting — yellow warnings are advisory only",
            "Download individual artifact packages or the complete bundle",
            "The readiness score is weighted across all 7 steps — aim for 85%+",
            "You can always go back to earlier steps to fix issues, then return here",
        ],
        "feeds": "Snowflake DDL, dbt models, Collibra import, docs, full JSON",
    },
}
