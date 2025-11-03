"""
ContextAnalyzer — processes Jira issue data and prepares structured input for the generator.
"""

import re
import logging
from atlassian_client.context_adapter import AtlassianContextAdapter


class ContextAnalyzer:
    def __init__(self, adapter: AtlassianContextAdapter):
        self.adapter = adapter
        self.logger = logging.getLogger(__name__)

    def extract_context(self, issue_key: str) -> dict:
        """Fetch and clean issue data from Jira."""
        self.logger.info(f"Fetching issue data for {issue_key}...")
        raw_data = self.adapter.get_issue_data(issue_key)

        if not raw_data:
            self.logger.warning(f"No data found for issue {issue_key}")
            return {}

        clean_data = self._clean_text(raw_data)
        return {"issue_key": issue_key, "context": clean_data}

    def _clean_text(self, data: dict) -> dict:
        """Normalize and sanitize Jira fields."""
        clean_fields = {}
        for key, value in data.items():
            if isinstance(value, str):
                clean_fields[key] = re.sub(r"\s+", " ", value.strip())
            else:
                clean_fields[key] = value
        return clean_fields
