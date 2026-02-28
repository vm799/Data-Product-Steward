# GDP Data Product Steward

A guided wizard for building enterprise data products with governance, quality, and export capabilities.

## Structure

```
data-product-builder-mvp/
├── app.py                  # Main Streamlit application
├── config.py               # Central configuration
├── state_manager.py        # Session state management
├── pages/                  # Wizard step pages
│   ├── 1_Business_Context.py
│   ├── 2_Data_Sources.py
│   ├── 3_Data_Model.py
│   ├── 4_Governance_Security.py
│   ├── 5_Data_Quality.py
│   ├── 6_Transformations.py
│   └── 7_Review_Export.py
├── core/                   # Backend engines
│   ├── scoring_engine.py
│   ├── validation_engine.py
│   ├── snowflake_generator.py
│   ├── collibra_generator.py
│   ├── dbt_generator.py
│   └── document_engine.py
├── components/             # Reusable UI components
│   ├── glossary_panel.py
│   ├── progress_tracker.py
│   └── canvas_preview.py
├── assets/                 # Static assets
├── requirements.txt
└── README.md
```

## Getting Started

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Steps

1. **Business Context** — Define purpose, domain, and stakeholders
2. **Data Sources** — Register source systems
3. **Data Model** — Design entities and schemas
4. **Governance & Security** — Set classification, access, and compliance
5. **Data Quality** — Configure quality thresholds and rules
6. **Transformations** — Define processing logic
7. **Review & Export** — Validate and generate artifacts (Snowflake DDL, dbt, Collibra, docs)
