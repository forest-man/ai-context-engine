"""
ContextScheduler — manages periodic context reanalysis and test regeneration.
"""

import logging
import time
from context_engine.analyzer import ContextAnalyzer
from context_engine.generator import TestCaseGenerator


class ContextScheduler:
    def __init__(self, analyzer: ContextAnalyzer, generator: TestCaseGenerator, interval: int = 3600):
        self.analyzer = analyzer
        self.generator = generator
        self.interval = interval
        self.logger = logging.getLogger(__name__)

    def run(self, issues: list[str]):
        """Continuously process listed issues at defined intervals."""
        self.logger.info("Starting context scheduler...")
        while True:
            for issue_key in issues:
                try:
                    self.logger.info(f"Reanalyzing issue {issue_key}")
                    context = self.analyzer.extract_context(issue_key)
                    self.generator.generate_test_case(context)
                except Exception as e:
                    self.logger.error(f"Error processing {issue_key}: {e}")

            self.logger.info(f"Sleeping for {self.interval} seconds...")
            time.sleep(self.interval)
