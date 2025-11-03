# ai-context-engine/atlassian_client/__init__.py
"""
Atlassian Client Package

Provides unified access to Jira/Xray APIs via REST or MCP adapters.
"""

from .rest_client import XrayRestClient as RestClient
from .mcp_client import AtlassianMCPClient as MCPClient
from .context_adapter import ContextAdapter

__all__ = ["RestClient", "MCPClient", "ContextAdapter"]
