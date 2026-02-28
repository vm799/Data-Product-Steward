"""
Collibra Generator
Produces metadata artifacts compatible with Collibra import formats.
"""

import json


class CollibraGenerator:
    """Generates Collibra-compatible metadata from the data product definition."""

    def __init__(self, product: dict):
        self.product = product

    def generate_asset_import(self) -> list:
        """Generate asset records for Collibra bulk import."""
        p = self.product
        assets = []

        # Data product asset
        assets.append({
            "resourceType": "Asset",
            "identifier": {
                "name": p.get("name", "Unnamed"),
                "domain": p.get("domain", ""),
            },
            "type": {"name": "Data Product"},
            "attributes": {
                "Description": [{"value": p.get("objective", "")}],
                "Classification": [{"value": p.get("classification", "")}],
                "PII": [{"value": str(p.get("pii", False))}],
                "Retention Policy": [{"value": p.get("retention_policy", "")}],
                "Geographic Scope": [{"value": p.get("geo_scope", "")}],
                "Consumers": [{"value": p.get("consumers", "")}],
            },
            "relations": {
                "Compliance": [{"name": f} for f in p.get("compliance_frameworks", [])],
            },
        })

        # Entity assets
        for entity in p.get("entities", []):
            entity_asset = {
                "resourceType": "Asset",
                "identifier": {
                    "name": entity.get("name", ""),
                    "domain": p.get("domain", ""),
                },
                "type": {"name": "Data Entity"},
                "attributes": {},
                "relations": {
                    "is part of": [{"name": p.get("name", "Unnamed")}],
                },
            }

            # Column-level assets
            for attr in entity.get("attributes", []):
                assets.append({
                    "resourceType": "Asset",
                    "identifier": {
                        "name": f"{entity['name']}.{attr['name']}",
                        "domain": p.get("domain", ""),
                    },
                    "type": {"name": "Data Attribute"},
                    "attributes": {
                        "Data Type": [{"value": attr.get("data_type", "")}],
                        "Description": [{"value": attr.get("description", "")}],
                        "PII": [{"value": str(attr.get("pii", False))}],
                        "Nullable": [{"value": str(attr.get("nullable", True))}],
                    },
                    "relations": {
                        "is part of": [{"name": entity.get("name", "")}],
                    },
                })

            assets.append(entity_asset)

        return assets

    def to_json(self) -> str:
        """Return the Collibra import payload as a JSON string."""
        return json.dumps(self.generate_asset_import(), indent=2)
