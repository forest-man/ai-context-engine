"""
Handles communication with Atlassian Xray Cloud via REST API.
"""

import requests
import logging
from typing import Optional, Dict, Any


class XrayRestClient:
    def __init__(self, base_url: str, client_id: str, client_secret: str):
        self.base_url = base_url.rstrip('/')
        self.client_id = client_id
        self.client_secret = client_secret
        self.token: Optional[str] = None

    def authenticate(self) -> bool:
        """Obtain bearer token from Atlassian API"""
        url = f"{self.base_url}/api/v2/authenticate"
        try:
            response = requests.post(url, json={
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }, timeout=10)
            response.raise_for_status()
            self.token = response.json()  # обычно API Xray возвращает просто строку токена
            if isinstance(self.token, dict):
                self.token = self.token.get("token") or next(iter(self.token.values()), None)
            logging.info("✅ Authenticated successfully with Xray Cloud")
            return True
        except Exception as e:
            logging.error(f"❌ Authentication failed: {e}")
            return False

    def _get_headers(self) -> Dict[str, str]:
        if not self.token:
            raise ValueError("Client not authenticated — call authenticate() first.")
        return {"Authorization": f"Bearer {self.token}"}

    def create_test_case(self, project_key: str, summary: str, description: str) -> Optional[Dict[str, Any]]:
        """Create a test case in Xray"""
        url = f"{self.base_url}/api/v2/test"
        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": "Test"}
            }
        }
        try:
            response = requests.post(url, json=payload, headers=self._get_headers(), timeout=15)
            response.raise_for_status()
            result = response.json()
            logging.info(f"✅ Created test case: {result.get('key', '<unknown>')}")
            return result
        except Exception as e:
            logging.error(f"❌ Failed to create test case: {e}")
            return None
