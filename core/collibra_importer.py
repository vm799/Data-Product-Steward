"""
Collibra Data Importer
Fetches existing data models from Collibra and converts them to Data Product format.
"""

from typing import Dict, List, Optional
from .collibra_client import CollibraClient


class CollibraImporter:
    """Import data models from Collibra into Data Product format."""

    def __init__(self, collibra_client: CollibraClient):
        """Initialize importer with Collibra client."""
        self.client = collibra_client

    def import_data_model(self, domain_name: str) -> Dict:
        """
        Import a complete data model from a Collibra domain.

        Args:
            domain_name: Name of the domain to import

        Returns:
            Dictionary with entities and attributes in Data Product format
        """
        try:
            assets = self.client.get_domain_assets(domain_name)
        except Exception as e:
            raise ValueError(f"Failed to fetch assets from domain '{domain_name}': {str(e)}")

        entities = []
        attributes_by_entity = {}

        # Process assets - separate entities from attributes
        for asset in assets:
            asset_type = asset.get("type", {}).get("name", "")
            asset_name = asset.get("name", "")
            asset_id = asset.get("id", "")

            if asset_type in ["Data Entity", "Table", "DataSet"]:
                entity = {
                    "name": asset_name.upper(),
                    "attributes": [],
                    "collibra_id": asset_id,
                    "description": asset.get("description", ""),
                }
                entities.append(entity)
                attributes_by_entity[asset_name] = entity

            elif asset_type in ["Data Attribute", "Column", "Field"]:
                # Find parent entity
                relations = self.client.get_asset_relations(asset_id)
                parent_entity = self._find_parent_entity(relations)

                if parent_entity:
                    attr = {
                        "name": asset_name.upper(),
                        "data_type": self._infer_data_type(asset),
                        "nullable": self._is_nullable(asset),
                        "pii": self._is_pii(asset),
                        "description": asset.get("description", ""),
                        "collibra_id": asset_id,
                    }
                    if parent_entity in attributes_by_entity:
                        attributes_by_entity[parent_entity]["attributes"].append(attr)

        return {
            "entities": entities,
            "import_source": "collibra",
            "import_domain": domain_name,
        }

    def import_data_sources(self, domain_name: str) -> List[Dict]:
        """
        Import data sources from Collibra.

        Args:
            domain_name: Domain name

        Returns:
            List of source configurations
        """
        sources = []
        try:
            assets = self.client.get_domain_assets(domain_name)
            for asset in assets:
                asset_type = asset.get("type", {}).get("name", "")
                if asset_type in ["Data Source", "System", "Database", "API"]:
                    source = {
                        "name": asset.get("name", ""),
                        "type": asset_type,
                        "description": asset.get("description", ""),
                        "collibra_id": asset.get("id", ""),
                        "attributes": asset.get("attributes", {}),
                    }
                    sources.append(source)
        except Exception as e:
            raise ValueError(f"Failed to import data sources: {str(e)}")

        return sources

    def import_governance_policies(self, domain_name: str) -> Dict:
        """
        Import governance and classification policies from Collibra.

        Args:
            domain_name: Domain name

        Returns:
            Dictionary with classification, compliance, and retention settings
        """
        governance = {
            "classification": None,
            "compliance_frameworks": [],
            "retention_policy": None,
        }

        try:
            assets = self.client.get_domain_assets(domain_name)
            for asset in assets:
                attrs = asset.get("attributes", {})

                # Extract classification
                if "Classification" in attrs:
                    classification = attrs["Classification"][0].get("value")
                    if classification:
                        governance["classification"] = classification

                # Extract compliance
                if "Compliance" in attrs:
                    for comp in attrs["Compliance"]:
                        gov_framework = comp.get("value")
                        if gov_framework:
                            governance["compliance_frameworks"].append(gov_framework)

                # Extract retention
                if "Retention Policy" in attrs:
                    retention = attrs["Retention Policy"][0].get("value")
                    if retention:
                        governance["retention_policy"] = retention

        except Exception as e:
            raise ValueError(f"Failed to import governance policies: {str(e)}")

        return governance

    def import_quality_rules(self, domain_name: str) -> List[Dict]:
        """
        Import data quality rules from Collibra.

        Args:
            domain_name: Domain name

        Returns:
            List of quality rules in Data Product format
        """
        rules = []
        try:
            assets = self.client.get_domain_assets(domain_name)
            for asset in assets:
                quality_rules = self.client.get_data_quality_rules(asset.get("id", ""))
                for rule in quality_rules:
                    converted_rule = {
                        "attribute": f"{asset.get('name', '')}.{rule.get('name', '')}",
                        "rule_type": rule.get("type", "custom"),
                        "rule_definition": rule.get("definition", ""),
                        "threshold": rule.get("threshold"),
                        "collibra_id": rule.get("id", ""),
                    }
                    rules.append(converted_rule)
        except Exception as e:
            # Quality rules might not be supported in all Collibra versions
            pass

        return rules

    def _find_parent_entity(self, relations: List[Dict]) -> Optional[str]:
        """Find parent entity from relations."""
        for relation in relations:
            if relation.get("relationType", "").lower() in ["is part of", "ispartof", "child of"]:
                return relation.get("targetAsset", {}).get("name")
        return None

    def _infer_data_type(self, asset: Dict) -> str:
        """Infer data type from Collibra asset metadata."""
        attrs = asset.get("attributes", {})

        # Check explicit data type attribute
        if "Data Type" in attrs:
            dtype = attrs["Data Type"][0].get("value", "").upper()
            if dtype:
                # Map to standard types
                if dtype.startswith("INT") or dtype.startswith("BIGINT"):
                    return "NUMBER"
                elif dtype.startswith("FLOAT") or dtype.startswith("DECIMAL"):
                    return "FLOAT"
                elif dtype.startswith("BOOL"):
                    return "BOOLEAN"
                elif "DATE" in dtype or "TIME" in dtype:
                    return "TIMESTAMP" if "TIME" in dtype else "DATE"
                elif dtype.startswith("VARCHAR") or dtype.startswith("TEXT"):
                    return "STRING"

        # Default to STRING
        return "STRING"

    def _is_nullable(self, asset: Dict) -> bool:
        """Determine if column is nullable."""
        attrs = asset.get("attributes", {})
        if "Nullable" in attrs:
            value = attrs["Nullable"][0].get("value", "").lower()
            return value != "false"
        return True

    def _is_pii(self, asset: Dict) -> bool:
        """Determine if asset contains PII."""
        attrs = asset.get("attributes", {})

        # Check explicit PII attribute
        if "PII" in attrs:
            value = attrs["PII"][0].get("value", "").lower()
            return value == "true"

        # Check name patterns
        name = asset.get("name", "").lower()
        pii_keywords = [
            "email",
            "phone",
            "ssn",
            "social_security",
            "credit_card",
            "password",
            "firstname",
            "lastname",
            "address",
            "dob",
            "date_of_birth",
        ]
        return any(keyword in name for keyword in pii_keywords)
