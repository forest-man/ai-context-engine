"""
TestCaseGenerator — uses AI prompts to create or update Xray test cases.
"""

import logging
from atlassian_client.context_adapter import AtlassianContextAdapter


class TestCaseGenerator:
    def __init__(self, adapter: AtlassianContextAdapter):
        self.adapter = adapter
        self.logger = logging.getLogger(__name__)

    def generate_test_case(self, issue_context: dict):
        """Generate or update an Xray test case based on issue context."""
        issue_key = issue_context.get("issue_key")
        context = issue_context.get("context")

        if not issue_key or not context:
            self.logger.error("Invalid issue context data.")
            return None

        self.logger.info(f"Generating Xray test case for {issue_key}...")

        # TODO: integrate with AI model (DARYL prompt library or OpenAI call)
        generated_steps = self._mock_generate_steps(context)

        return self.adapter.create_or_update_test_case(issue_key, generated_steps)

    def _mock_generate_steps(self, context: dict):
        """Placeholder logic for test step generation."""
        summary = context.get("summary", "Unnamed issue")
        return [
            {"action": f"Open issue: {summary}", "expected": "Issue loads successfully"},
            {"action": "Review description", "expected": "Details match acceptance criteria"},
        ]
