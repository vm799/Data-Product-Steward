"""
Collibra API Client Wrapper
Handles authentication, asset retrieval, and metadata operations.
"""

import os
from typing import Optional, Dict, List
import time
import json

try:
    import requests
    from requests.auth import HTTPBasicAuth
except ImportError:
    requests = None

from config import COLLIBRA_CONFIG


class CollibraClient:
    """Wrapper around Collibra REST API with retry logic and caching."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        """Initialize Collibra client."""
        if not requests:
            raise ImportError("requests package not installed. Install with: pip install requests")

        self.base_url = base_url or COLLIBRA_CONFIG.get("base_url") or os.getenv("COLLIBRA_BASE_URL")
        self.username = username or COLLIBRA_CONFIG.get("username") or os.getenv("COLLIBRA_USERNAME")
        self.password = password or COLLIBRA_CONFIG.get("password") or os.getenv("COLLIBRA_PASSWORD")

        if not self.base_url:
            raise ValueError("COLLIBRA_BASE_URL not configured")
        if not self.username or not self.password:
            raise ValueError("COLLIBRA_USERNAME and COLLIBRA_PASSWORD not configured")

        self.auth = HTTPBasicAuth(self.username, self.password)
        self.timeout = COLLIBRA_CONFIG.get("timeout", 30)
        self.max_retries = COLLIBRA_CONFIG.get("max_retries", 3)
        self.verify_ssl = COLLIBRA_CONFIG.get("verify_ssl", True)
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.verify = self.verify_ssl

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        retry_count: int = 0,
    ) -> Dict:
        """
        Make an HTTP request to Collibra API with retry logic.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            data: Request body
            retry_count: Current retry attempt

        Returns:
            JSON response
        """
        url = f"{self.base_url}/api/v1/{endpoint}"
        headers = {"Content-Type": "application/json"}

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429 and retry_count < self.max_retries:
                # Rate limited - retry with backoff
                wait_time = 2 ** retry_count
                time.sleep(wait_time)
                return self._request(method, endpoint, params, data, retry_count + 1)
            raise ValueError(f"Collibra API error {e.response.status_code}: {str(e)}")
        except requests.exceptions.ConnectionError as e:
            if retry_count < self.max_retries:
                wait_time = 2 ** retry_count
                time.sleep(wait_time)
                return self._request(method, endpoint, params, data, retry_count + 1)
            raise ValueError(f"Connection error after {self.max_retries} retries: {str(e)}")
        except requests.exceptions.Timeout as e:
            if retry_count < self.max_retries:
                wait_time = 2 ** retry_count
                time.sleep(wait_time)
                return self._request(method, endpoint, params, data, retry_count + 1)
            raise ValueError(f"Timeout after {self.max_retries} retries: {str(e)}")

    def get_assets(
        self,
        asset_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict]:
        """
        Retrieve assets from Collibra.

        Args:
            asset_type: Filter by asset type (e.g., 'Data Entity', 'Data Attribute')
            limit: Number of results to return
            offset: Pagination offset

        Returns:
            List of asset objects
        """
        params = {"limit": limit, "offset": offset}
        if asset_type:
            params["type"] = asset_type

        response = self._request("GET", "assets", params=params)
        return response.get("results", [])

    def search_assets(self, query: str, limit: int = 50) -> List[Dict]:
        """
        Search for assets by name or description.

        Args:
            query: Search query
            limit: Max results

        Returns:
            List of matching assets
        """
        params = {"query": query, "limit": limit}
        response = self._request("GET", "assets/search", params=params)
        return response.get("results", [])

    def get_asset(self, asset_id: str) -> Dict:
        """
        Get a single asset by ID.

        Args:
            asset_id: Asset UUID

        Returns:
            Asset object with full details
        """
        return self._request("GET", f"assets/{asset_id}")

    def get_asset_attributes(self, asset_id: str) -> Dict:
        """
        Get all attributes of an asset.

        Args:
            asset_id: Asset UUID

        Returns:
            Dictionary of attribute name -> values
        """
        asset = self.get_asset(asset_id)
        return asset.get("attributes", {})

    def get_asset_relations(self, asset_id: str) -> List[Dict]:
        """
        Get relations/lineage for an asset.

        Args:
            asset_id: Asset UUID

        Returns:
            List of related assets
        """
        response = self._request("GET", f"assets/{asset_id}/relations")
        return response.get("relations", [])

    def get_domain_assets(self, domain_name: str) -> List[Dict]:
        """
        Get all assets in a domain.

        Args:
            domain_name: Domain name

        Returns:
            List of assets in that domain
        """
        response = self._request("GET", "assets", params={"domainName": domain_name})
        return response.get("results", [])

    def get_data_quality_rules(self, asset_id: str) -> List[Dict]:
        """
        Get data quality rules associated with an asset.

        Args:
            asset_id: Asset UUID

        Returns:
            List of quality rules
        """
        try:
            response = self._request("GET", f"assets/{asset_id}/quality-rules")
            return response.get("results", [])
        except ValueError:
            # API may not support this endpoint in all versions
            return []

    def create_asset(
        self,
        name: str,
        asset_type: str,
        domain: str,
        attributes: Optional[Dict] = None,
        description: Optional[str] = None,
    ) -> Dict:
        """
        Create a new asset in Collibra.

        Args:
            name: Asset name
            asset_type: Type of asset
            domain: Domain name
            attributes: Optional attribute dictionary
            description: Asset description

        Returns:
            Created asset object
        """
        payload = {
            "name": name,
            "type": asset_type,
            "domain": domain,
        }
        if description:
            payload["description"] = description
        if attributes:
            payload["attributes"] = attributes

        return self._request("POST", "assets", data=payload)

    def update_asset(self, asset_id: str, updates: Dict) -> Dict:
        """
        Update an existing asset.

        Args:
            asset_id: Asset UUID
            updates: Dictionary of fields to update

        Returns:
            Updated asset object
        """
        return self._request("PATCH", f"assets/{asset_id}", data=updates)

    def test_connection(self) -> bool:
        """
        Test connectivity to Collibra API.

        Returns:
            True if connection successful
        """
        try:
            self._request("GET", "assets", params={"limit": 1})
            return True
        except Exception:
            return False
