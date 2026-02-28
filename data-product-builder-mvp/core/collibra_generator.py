"""
Collibra Generator
Produces metadata artifacts compatible with Collibra import formats.
"""

import json


class CollibraGenerator:
    """Generates Collibra-compatible metadata from the data product definition."""

    def __init__(self, state_snapshot: dict):
        self.state = state_snapshot

    def generate_asset_import(self) -> list[dict]:
        """Generate asset records for Collibra bulk import."""
        ctx = self.state.get("business_context", {})
        assets = []

        # Data product asset
        assets.append({
            "resourceType": "Asset",
            "identifier": {"name": ctx.get("product_name", "Unnamed"), "domain": ctx.get("domain", "")},
            "type": {"name": "Data Product"},
            "attributes": {
                "Description": [{"value": ctx.get("description", "")}],
                "Business Value": [{"value": ctx.get("business_value", "")}],
            },
            "relations": {
                "Owner": [{"name": ctx.get("owner", "")}],
            },
        })

        # Entity assets
        model = self.state.get("data_model", {})
        for entity in model.get("entities", []):
            assets.append({
                "resourceType": "Asset",
                "identifier": {"name": entity.get("name", ""), "domain": ctx.get("domain", "")},
                "type": {"name": "Data Entity"},
                "attributes": {
                    "Description": [{"value": entity.get("description", "")}],
                    "Grain": [{"value": entity.get("grain", "")}],
                },
            })

        return assets

    def to_json(self) -> str:
        """Return the Collibra import payload as a JSON string."""
        return json.dumps(self.generate_asset_import(), indent=2)
