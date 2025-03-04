from typing import List

from athena.models.athena_test_suite_config import AthenaTestSuiteConfig
from athena.models.test_result import TestResult
from athena.models.test_suite_summary import TestSuiteSummary
from athena.protocols.report_plugins_manager_protocol import (
    ReportPluginsManagerProtocol,
)


class ReportService:
    """Component responsible for generating reports."""

    def __init__(self, plugin_manager: ReportPluginsManagerProtocol) -> None:
        self.plugin_manager = plugin_manager

    def generate_reports(
        self, config: AthenaTestSuiteConfig, results: List[TestResult]
    ) -> None:
        """Generate reports using the configured reporters."""
        summary = TestSuiteSummary(results=results)
        for report in config.reports:
            self.plugin_manager.report(report, summary)
