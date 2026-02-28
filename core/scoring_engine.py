"""
Scoring Engine
Calculates a readiness score for the data product based on completeness.
"""


class ScoringEngine:
    """Computes a weighted readiness score across all wizard steps."""

    def __init__(self, product: dict):
        self.product = product

    def step_scores(self) -> dict:
        """Return individual step scores (0.0-1.0)."""
        p = self.product
        scores = {}

        # Business Context
        fields = [p.get("name"), p.get("domain"), p.get("objective"), p.get("consumers")]
        scores["business_context"] = sum(1 for f in fields if f) / len(fields)

        # Data Sources
        scores["data_sources"] = min(len(p.get("sources", [])) / 1, 1.0)

        # Data Model
        entities = p.get("entities", [])
        if entities:
            attr_counts = [len(e.get("attributes", [])) for e in entities]
            scores["data_model"] = 1.0 if all(c > 0 for c in attr_counts) else 0.5
        else:
            scores["data_model"] = 0.0

        # Governance
        gov_fields = [p.get("classification"), p.get("retention_policy")]
        scores["governance_security"] = sum(1 for f in gov_fields if f) / len(gov_fields)

        # Data Quality
        scores["data_quality"] = 1.0 if p.get("quality_rules") else 0.0

        # Transformations
        scores["transformations"] = min(len(p.get("transformations", [])) / 1, 1.0)

        return scores

    def overall_score(self) -> int:
        """Compute the overall readiness score (0-100)."""
        scores = self.step_scores()
        weights = {
            "business_context": 0.15,
            "data_sources": 0.15,
            "data_model": 0.15,
            "governance_security": 0.20,
            "data_quality": 0.20,
            "transformations": 0.15,
        }
        total = sum(scores.get(k, 0) * w for k, w in weights.items())
        return int(total * 100)
