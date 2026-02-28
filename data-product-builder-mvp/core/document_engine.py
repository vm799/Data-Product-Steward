"""
Document Engine
Generates human-readable documentation for the data product.
"""


class DocumentEngine:
    """Produces Markdown documentation from the data product definition."""

    def __init__(self, state_snapshot: dict):
        self.state = state_snapshot

    def generate_markdown(self) -> str:
        """Generate a complete Markdown document for the data product."""
        sections = [
            self._title_section(),
            self._business_context_section(),
            self._data_sources_section(),
            self._data_model_section(),
            self._governance_section(),
            self._data_quality_section(),
            self._transformations_section(),
        ]
        return "\n\n---\n\n".join(s for s in sections if s)

    def _title_section(self) -> str:
        ctx = self.state.get("business_context", {})
        name = ctx.get("product_name", "Untitled Data Product")
        return f"# {name}\n\n{ctx.get('description', '')}"

    def _business_context_section(self) -> str:
        ctx = self.state.get("business_context", {})
        lines = ["## Business Context"]
        lines.append(f"- **Domain:** {ctx.get('domain', 'N/A')}")
        lines.append(f"- **Owner:** {ctx.get('owner', 'N/A')}")
        lines.append(f"- **Stakeholders:** {ctx.get('stakeholders', 'N/A')}")
        lines.append(f"\n### Business Value\n{ctx.get('business_value', 'N/A')}")
        lines.append(f"\n### Use Cases\n{ctx.get('use_cases', 'N/A')}")
        return "\n".join(lines)

    def _data_sources_section(self) -> str:
        sources = self.state.get("data_sources", [])
        lines = ["## Data Sources"]
        if not sources:
            lines.append("No data sources defined.")
            return "\n".join(lines)
        for src in sources:
            lines.append(f"- **{src['name']}** ({src['type']}) — {src['refresh_frequency']}")
        return "\n".join(lines)

    def _data_model_section(self) -> str:
        model = self.state.get("data_model", {})
        entities = model.get("entities", [])
        lines = ["## Data Model"]
        for ent in entities:
            lines.append(f"\n### {ent['name']}")
            lines.append(f"{ent.get('description', '')}")
            lines.append(f"- **Primary Key:** {ent.get('primary_key', 'N/A')}")
            lines.append(f"- **Grain:** {ent.get('grain', 'N/A')}")
            if ent.get("columns"):
                lines.append("\n| Column | Type |")
                lines.append("|--------|------|")
                for col in ent["columns"]:
                    lines.append(f"| {col['name']} | {col['type']} |")
        return "\n".join(lines)

    def _governance_section(self) -> str:
        gov = self.state.get("governance_security", {})
        lines = ["## Governance & Security"]
        lines.append(f"- **Classification:** {gov.get('data_classification', 'N/A')}")
        lines.append(f"- **PII Present:** {'Yes' if gov.get('pii_present') else 'No'}")
        lines.append(f"- **Retention:** {gov.get('retention_policy', 'N/A')}")
        lines.append(f"- **Access Roles:** {gov.get('access_roles', 'N/A')}")
        frameworks = gov.get("compliance_frameworks", [])
        lines.append(f"- **Compliance:** {', '.join(frameworks) if frameworks else 'N/A'}")
        return "\n".join(lines)

    def _data_quality_section(self) -> str:
        dq = self.state.get("data_quality", {})
        lines = ["## Data Quality"]
        lines.append(f"- **Completeness:** {dq.get('completeness', 'N/A')}")
        lines.append(f"- **Accuracy:** {dq.get('accuracy', 'N/A')}")
        lines.append(f"- **Timeliness SLA:** {dq.get('timeliness_hours', 'N/A')} hours")
        lines.append(f"- **Uniqueness:** {dq.get('uniqueness', 'N/A')}")
        if dq.get("custom_rules"):
            lines.append(f"\n### Custom Rules\n{dq['custom_rules']}")
        return "\n".join(lines)

    def _transformations_section(self) -> str:
        transforms = self.state.get("transformations", [])
        lines = ["## Transformations"]
        if not transforms:
            lines.append("No transformations defined.")
            return "\n".join(lines)
        for t in transforms:
            lines.append(f"\n### {t['name']} ({t['type']})")
            lines.append(f"{t['source_entity']} → {t['target_entity']}")
            lines.append(f"\n{t.get('description', '')}")
        return "\n".join(lines)
