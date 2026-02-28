# GDP Data Product Steward

**Governed. Structured. Production-Ready.**

A guided wizard that collapses weeks of data product requirements gathering into a single, structured session — generating Snowflake DDL, dbt models, Collibra metadata, and governance documentation automatically.

## Structure

```
├── streamlit_app.py          # Main entry point & dashboard
├── state_manager.py          # Unified session state management
├── config.py                 # Central configuration
├── requirements.txt
├── pages/
│   ├── 1_Business_Context.py # Domain, objective, regulatory detection
│   ├── 2_Data_Sources.py     # Source systems, SLAs, risk flags
│   ├── 3_Data_Model.py       # Entities, attributes, PII tagging
│   ├── 4_Governance_Security.py # Classification, retention, compliance
│   ├── 5_Data_Quality.py     # Quality thresholds & monitoring
│   ├── 6_Transformations.py  # Processing logic & steps
│   └── 7_Review_Export.py    # Validation, scoring, artifact generation
├── components/
│   └── sidebar.py            # Shared progress tracker & glossary
└── core/
    ├── snowflake_generator.py # DDL, masking policies, secure views, grants
    ├── dbt_generator.py       # dbt model SQL & schema.yml
    ├── collibra_generator.py  # Collibra-compatible metadata import
    ├── document_engine.py     # Markdown documentation
    ├── validation_engine.py   # Completeness & policy validation
    └── scoring_engine.py      # Weighted readiness scoring
```

## Getting Started

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## What It Replaces

| Before | After |
|--------|-------|
| 4+ workshops | 1 guided session |
| 6 spreadsheet versions | Structured session state |
| Manual DDL writing | Auto-generated Snowflake DDL |
| Governance chasing definitions | PII auto-detection + masking policies |
| Separate Collibra onboarding | Collibra import JSON generated |
| Manual dbt scaffolding | dbt models + schema.yml generated |

## Generated Artifacts

- **Snowflake DDL** — CREATE TABLE with types, nullability, comments
- **Masking Policies** — Auto-generated for PII attributes
- **Secure Views** — Enforced for Restricted/Confidential classification
- **Access Grants** — Role-based GRANT statements
- **dbt Models** — SQL models + schema.yml with tests
- **Collibra Metadata** — Bulk import JSON (product, entity, attribute level)
- **Documentation** — Complete Markdown specification
