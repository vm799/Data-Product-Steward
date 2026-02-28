"""
Per-step contextual guidance shown in the sidebar.
Each step has: why it matters, practical tips, and what it feeds into.
"""

STEP_GUIDES = {
    1: {
        "title": "Why Business Context?",
        "why": (
            "Defining your domain and regulatory scope **upfront** determines which "
            "governance policies, compliance frameworks, and security controls are "
            "automatically applied to every artifact generated."
        ),
        "tips": [
            "Pick a descriptive name like `Investor_Position_Summary`",
            "Regulatory scope is auto-detected from domain + geography",
            "Be specific about consumers — this drives access roles later",
        ],
        "feeds": "Regulatory detection, Collibra domain mapping, document header",
    },
    2: {
        "title": "Why Register Sources?",
        "why": (
            "Every data product needs accountable ownership. Registering sources with "
            "SLAs and criticality enables **automatic governance alerts** — e.g. external "
            "sources trigger enhanced due diligence."
        ),
        "tips": [
            "Every source needs a named Data Owner — no orphan data",
            "High-criticality sources without SLAs get flagged automatically",
            "External/Vendor sources require enhanced due diligence",
        ],
        "feeds": "dbt source definitions, lineage documentation, risk assessment",
    },
    3: {
        "title": "Why Build the Data Model?",
        "why": (
            "Entities and attributes are the backbone. **PII tagging here drives "
            "automatic masking policy generation** in Snowflake — one checkbox creates "
            "a complete security policy."
        ),
        "tips": [
            "Names are auto-uppercased to match Snowflake convention",
            "Tag ALL attributes containing personal data as PII",
            "Descriptions become column COMMENT in the generated DDL",
        ],
        "feeds": "Snowflake DDL, dbt schema.yml, Collibra attributes, masking policies",
    },
    4: {
        "title": "Why Set Governance?",
        "why": (
            "Classification determines security controls: **Restricted** = secure views "
            "+ row-level security. **Confidential** = column masking. This is not "
            "optional — it directly shapes what gets generated."
        ),
        "tips": [
            "If PII exists, add at least GDPR or CCPA to compliance",
            "Restricted is the strongest tier — use for MNPI and PII",
            "Access roles map directly to Snowflake GRANT statements",
        ],
        "feeds": "Masking policies, secure views, access grants, compliance metadata",
    },
    5: {
        "title": "Why Define Quality Rules?",
        "why": (
            "Quality thresholds define what **'good enough'** means. These become "
            "automated checks in your data pipeline — if completeness drops below "
            "threshold, alerts fire."
        ),
        "tips": [
            "95% completeness is the industry baseline — adjust to your SLAs",
            "Set timeliness based on source SLAs from Step 2",
            "Custom rules become dbt tests in generated models",
        ],
        "feeds": "dbt tests, monitoring rules, quality documentation",
    },
    6: {
        "title": "Why Document Transformations?",
        "why": (
            "Transformation logic creates an **audit trail** and enables automatic "
            "dbt model generation. Regulators require lineage — this is how you prove it."
        ),
        "tips": [
            "Reference entity names from Step 3 for lineage integrity",
            "SQL logic becomes the body of generated dbt models",
            "Chain steps: source -> staging -> final for clarity",
        ],
        "feeds": "dbt model SQL, transformation docs, lineage mapping",
    },
    7: {
        "title": "Your Quality Gate",
        "why": (
            "This is the final checkpoint. Validation ensures your data product "
            "definition is **complete and consistent** before generating deployment "
            "artifacts."
        ),
        "tips": [
            "Fix all errors before exporting — warnings are advisory",
            "Download individual artifacts or the complete package",
            "Readiness score is weighted across all previous steps",
        ],
        "feeds": "Snowflake DDL, dbt models, Collibra import, docs, full JSON",
    },
}
