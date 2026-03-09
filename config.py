"""
Data Product Builder — Configuration
"""

import os

APP_CONFIG = {
    "title": "Data Product Builder — Asset Management",
    "icon": "📊",
    "layout": "wide",
    "version": "1.0.0",
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

CLASSIFICATION_OPTIONS = ["Public", "Internal", "Confidential", "Restricted"]

RETENTION_OPTIONS = ["30 Days", "90 Days", "1 Year", "3 Years", "7 Years", "Indefinite"]

QUALITY_THRESHOLDS = {
    "completeness": 95,
    "accuracy": 99,
    "timeliness_hours": 24,
    "uniqueness": 100,
}

SCORING_WEIGHTS = {
    "business_context": 0.15,
    "data_sources": 0.15,
    "data_model": 0.15,
    "governance_security": 0.20,
    "data_quality": 0.20,
    "transformations": 0.15,
}

# ── API Configuration ────────────────────────────────────────────────────

# OpenAI API settings
OPENAI_CONFIG = {
    "api_key": os.getenv("OPENAI_API_KEY", ""),
    "base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    "model": os.getenv("OPENAI_MODEL", "gpt-4-turbo"),
    "timeout": 30,
    "max_retries": 3,
}

# Collibra API settings
COLLIBRA_CONFIG = {
    "base_url": os.getenv("COLLIBRA_BASE_URL", ""),
    "username": os.getenv("COLLIBRA_USERNAME", ""),
    "password": os.getenv("COLLIBRA_PASSWORD", ""),
    "timeout": 30,
    "max_retries": 3,
    "verify_ssl": True,
}

# Caching settings for Collibra data
CACHE_CONFIG = {
    "ttl_seconds": 3600,  # 1 hour cache
    "max_size_mb": 100,
}

