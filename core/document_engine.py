"""
Document Engine
Generates human-readable Markdown documentation for the data product.
"""


class DocumentEngine:
    """Produces Markdown documentation from the data product definition."""

    def __init__(self, product: dict):
        self.product = product

    def generate_markdown(self) -> str:
        """Generate a complete Markdown document."""
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
        p = self.product
        name = p.get("name", "Untitled Data Product")
        return f"# {name}\n\n**Domain:** {p.get('domain', 'N/A')} | **Scope:** {p.get('geo_scope', 'N/A')}"

    def _business_context_section(self) -> str:
        p = self.product
        lines = ["## Business Context"]
        lines.append(f"- **Domain:** {p.get('domain', 'N/A')}")
        lines.append(f"- **Objective:** {p.get('objective', 'N/A')}")
        lines.append(f"- **Consumers:** {p.get('consumers', 'N/A')}")
        if p.get("regulatory_scope"):
            lines.append(f"- **Regulatory Scope:** {', '.join(p['regulatory_scope'])}")
        return "\n".join(lines)

    def _data_sources_section(self) -> str:
        sources = self.product.get("sources", [])
        lines = ["## Data Sources"]
        if not sources:
            lines.append("No data sources defined.")
            return "\n".join(lines)
        lines.append("| Source | Type | Owner | Frequency | Criticality |")
        lines.append("|--------|------|-------|-----------|-------------|")
        for src in sources:
            lines.append(
                f"| {src['name']} | {src['type']} | {src['owner']} | "
                f"{src['frequency']} | {src['criticality']} |"
            )
        return "\n".join(lines)

    def _data_model_section(self) -> str:
        entities = self.product.get("entities", [])
        lines = ["## Data Model"]
        if not entities:
            lines.append("No entities defined.")
            return "\n".join(lines)
        for ent in entities:
            lines.append(f"\n### {ent['name']}")
            attrs = ent.get("attributes", [])
            if attrs:
                lines.append("| Attribute | Type | Nullable | PII | Description |")
                lines.append("|-----------|------|----------|-----|-------------|")
                for a in attrs:
                    pii = "Yes" if a.get("pii") else "No"
                    null = "Yes" if a.get("nullable") else "No"
                    lines.append(
                        f"| {a['name']} | {a['data_type']} | {null} | {pii} | {a.get('description', '')} |"
                    )
        return "\n".join(lines)

    def _governance_section(self) -> str:
        p = self.product
        lines = ["## Governance & Security"]
        lines.append(f"- **Classification:** {p.get('classification', 'N/A')}")
        lines.append(f"- **PII Present:** {'Yes' if p.get('pii') else 'No'}")
        lines.append(f"- **Retention:** {p.get('retention_policy', 'N/A')}")
        lines.append(f"- **Access Roles:** {p.get('access_roles', 'N/A')}")
        frameworks = p.get("compliance_frameworks", [])
        lines.append(f"- **Compliance:** {', '.join(frameworks) if frameworks else 'N/A'}")
        return "\n".join(lines)

    def _data_quality_section(self) -> str:
        qr = self.product.get("quality_rules", {})
        lines = ["## Data Quality"]
        if not qr:
            lines.append("No quality rules defined.")
            return "\n".join(lines)
        lines.append(f"- **Completeness:** {qr.get('completeness', 'N/A')}%")
        lines.append(f"- **Accuracy:** {qr.get('accuracy', 'N/A')}%")
        lines.append(f"- **Timeliness SLA:** {qr.get('timeliness_hours', 'N/A')} hours")
        lines.append(f"- **Uniqueness:** {qr.get('uniqueness', 'N/A')}%")
        if qr.get("monitoring_channel"):
            lines.append(f"- **Alerting:** {qr['monitoring_channel']}")
        if qr.get("custom_rules"):
            lines.append(f"\n### Custom Rules\n```\n{qr['custom_rules']}\n```")
        return "\n".join(lines)

    def _transformations_section(self) -> str:
        transforms = self.product.get("transformations", [])
        lines = ["## Transformations"]
        if not transforms:
            lines.append("No transformations defined.")
            return "\n".join(lines)
        for t in transforms:
            lines.append(f"\n### {t['name']} ({t['type']})")
            lines.append(f"`{t.get('source_entity', '')}` → `{t.get('target_entity', '')}`")
            if t.get("description"):
                lines.append(f"\n{t['description']}")
            if t.get("logic"):
                lines.append(f"\n```sql\n{t['logic']}\n```")
        return "\n".join(lines)
