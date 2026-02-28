"""
Scoring Engine
Calculates a readiness score for the data product based on completeness
and quality of each wizard step.
"""

from config import SCORING_WEIGHTS


class ScoringEngine:
    """Computes a weighted readiness score across all wizard steps."""

    def __init__(self, state_snapshot: dict):
        self.state = state_snapshot

    def score_step(self, step_key: str) -> float:
        """Return a 0-1 score for a single step based on field completeness."""
        data = self.state.get(step_key)
        if not data:
            return 0.0

        if isinstance(data, dict):
            filled = sum(1 for v in data.values() if v)
            total = len(data)
            return filled / total if total > 0 else 0.0

        if isinstance(data, list):
            return 1.0 if len(data) > 0 else 0.0

        return 0.0

    def overall_score(self) -> float:
        """Compute the weighted overall readiness score (0-100)."""
        total = 0.0
        for step_key, weight in SCORING_WEIGHTS.items():
            total += self.score_step(step_key) * weight
        return round(total * 100, 1)

    def step_scores(self) -> dict:
        """Return individual step scores."""
        return {key: self.score_step(key) for key in SCORING_WEIGHTS}
