"""
Validation Engine
Validates data product definitions for completeness, consistency, and policy compliance.
"""


class ValidationEngine:
    """Runs validation checks against the data product definition."""

    def __init__(self, product: dict):
        self.product = product
        self.errors = []
        self.warnings = []

    def validate(self) -> dict:
        """Run all validations and return results."""
        self._validate_business_context()
        self._validate_data_sources()
        self._validate_data_model()
        self._validate_governance()
        self._validate_data_quality()
        self._validate_transformations()
        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
            "score": self._compute_score(),
        }

    def _validate_business_context(self):
        p = self.product
        if not p.get("name"):
            self.errors.append("Product name is required.")
        if not p.get("domain"):
            self.errors.append("Business domain is required.")
        if not p.get("objective"):
            self.errors.append("Business objective is required.")
        if not p.get("consumers"):
            self.warnings.append("No primary consumers specified.")

    def _validate_data_sources(self):
        sources = self.product.get("sources", [])
        if not sources:
            self.errors.append("At least one data source is required.")
        for src in sources:
            if src.get("criticality") == "High" and not src.get("sla_required"):
                self.warnings.append(
                    f"Source '{src['name']}' is high criticality without an SLA."
                )

    def _validate_data_model(self):
        entities = self.product.get("entities", [])
        if not entities:
            self.errors.append("At least one entity must be defined.")
        for ent in entities:
            if not ent.get("attributes"):
                self.warnings.append(f"Entity '{ent['name']}' has no attributes defined.")

    def _validate_governance(self):
        p = self.product
        if not p.get("classification"):
            self.warnings.append("Data classification is not set.")
        if p.get("pii") and not p.get("compliance_frameworks"):
            self.warnings.append("PII detected but no compliance frameworks selected.")
        if p.get("classification") == "Restricted" and not p.get("access_roles"):
            self.warnings.append("Restricted classification requires explicit access roles.")

    def _validate_data_quality(self):
        qr = self.product.get("quality_rules", {})
        if not qr:
            self.warnings.append("No data quality rules defined.")

    def _validate_transformations(self):
        if not self.product.get("transformations"):
            self.warnings.append("No transformations defined.")

    def _compute_score(self) -> int:
        """Compute a readiness score (0-100)."""
        total = 7
        score = 0
        p = self.product

        if p.get("name") and p.get("domain") and p.get("objective"):
            score += 1
        if p.get("sources"):
            score += 1
        if any(len(e.get("attributes", [])) > 0 for e in p.get("entities", [])):
            score += 1
        if p.get("classification") and p.get("retention_policy"):
            score += 1
        if p.get("quality_rules"):
            score += 1
        if p.get("transformations"):
            score += 1
        if len(self.errors) == 0:
            score += 1

        return int(score / total * 100)
