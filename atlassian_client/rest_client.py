"""
Handles communication with Atlassian Xray Cloud via REST API.
"""

import requests
import logging

class XrayRestClient:
    def __init__(self, base_url, client_id, client_secret):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None

    def authenticate(self):
        """Obtain bearer token from Atlassian API"""
        url = f"{self.base_url}/api/v2/authenticate"
        response = requests.post(url, json={
            "client_id": self.client_id,
            "client_secret": self.client_secret
        })
        response.raise_for_status()
        self.token = response.json()
        logging.info("Authenticated successfully with Xray Cloud")

    def create_test_case(self, project_key, summary, description):
        """Create a test case in Xray"""
        url = f"{self.base_url}/api/v2/test"
        headers = {"Authorization": f"Bearer {self.token}"}
        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": "Test"}
            }
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
