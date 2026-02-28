"""
Data Product Builder MVP - Configuration
Central configuration for the application.
"""

APP_CONFIG = {
    "title": "Data Product Builder",
    "icon": "🏗️",
    "layout": "wide",
    "version": "0.1.0",
}

STEPS = [
    {"key": "business_context", "label": "Business Context", "page": 1},
    {"key": "data_sources", "label": "Data Sources", "page": 2},
    {"key": "data_model", "label": "Data Model", "page": 3},
    {"key": "governance_security", "label": "Governance & Security", "page": 4},
    {"key": "data_quality", "label": "Data Quality", "page": 5},
    {"key": "transformations", "label": "Transformations", "page": 6},
    {"key": "review_export", "label": "Review & Export", "page": 7},
]

SCORING_WEIGHTS = {
    "business_context": 0.15,
    "data_sources": 0.15,
    "data_model": 0.15,
    "governance_security": 0.20,
    "data_quality": 0.20,
    "transformations": 0.15,
}

QUALITY_THRESHOLDS = {
    "completeness": 0.95,
    "accuracy": 0.99,
    "timeliness_hours": 24,
    "uniqueness": 1.0,
}
