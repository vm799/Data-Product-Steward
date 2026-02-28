"""
Validation Engine
Validates data product definitions for completeness, consistency, and policy compliance.
"""


class ValidationEngine:
    """Runs validation checks against the data product definition."""

    def __init__(self, state_snapshot: dict):
        self.state = state_snapshot
        self.errors = []
        self.warnings = []

    def validate(self) -> dict:
        """Run all validations and return results."""
        self._validate_business_context()
        self._validate_data_sources()
        self._validate_data_model()
        self._validate_governance()
        self._validate_data_quality()
        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
        }

    def _validate_business_context(self):
        ctx = self.state.get("business_context", {})
        if not ctx.get("product_name"):
            self.errors.append("Business context: product name is required.")
        if not ctx.get("owner"):
            self.warnings.append("Business context: no owner specified.")

    def _validate_data_sources(self):
        sources = self.state.get("data_sources", [])
        if not sources:
            self.errors.append("At least one data source is required.")

    def _validate_data_model(self):
        model = self.state.get("data_model", {})
        entities = model.get("entities", [])
        if not entities:
            self.errors.append("At least one entity must be defined in the data model.")
        for ent in entities:
            if not ent.get("primary_key"):
                self.warnings.append(f"Entity '{ent.get('name', '?')}' has no primary key.")

    def _validate_governance(self):
        gov = self.state.get("governance_security", {})
        if gov.get("pii_present") and not gov.get("compliance_frameworks"):
            self.warnings.append(
                "PII is present but no compliance frameworks are selected."
            )

    def _validate_data_quality(self):
        dq = self.state.get("data_quality", {})
        if not dq:
            self.warnings.append("No data quality rules have been defined.")
