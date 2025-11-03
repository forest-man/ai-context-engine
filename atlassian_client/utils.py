# atlassian_client/utils.py
"""
Utility functions for Atlassian API clients.
Includes helpers for logging, authentication, and HTTP response handling.
"""

import os
import logging
import requests
from typing import Optional, Dict, Any

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


def get_env_var(name: str, default: Optional[str] = None) -> str:
    """
    Safely retrieve environment variable.
    """
    value = os.getenv(name, default)
    if value is None:
        logger.warning(f"Environment variable '{name}' is not set.")
    return value


def create_auth_header(client_id: str, client_secret: str) -> Dict[str, str]:
    """
    Create an authorization header for Atlassian API requests.
    """
    import base64
    token = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


def safe_request(
    method: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Any] = None,
    json: Optional[Any] = None,
    timeout: int = 15,
) -> requests.Response:
    """
    Execute an HTTP request with error handling and logging.
    """
    try:
        logger.info(f"→ {method.upper()} {url}")
        response = requests.request(method, url, headers=headers, data=data, json=json, timeout=timeout)
        response.raise_for_status()
        logger.info(f"✓ Success: {response.status_code}")
        return response
    except requests.RequestException as e:
        logger.error(f"✗ Request failed: {e}")
        raise


def extract_json(response: requests.Response) -> Any:
    """
    Extract and return JSON from a response object.
    """
    try:
        return response.json()
    except ValueError:
        logger.error("Failed to decode JSON from response.")
        return None
