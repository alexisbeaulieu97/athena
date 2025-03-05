from typing import Protocol, runtime_checkable

from athena.models.test_suite_config import TestSuiteConfig
from athena.models.test_suite_summary import TestSuiteSummary


@runtime_checkable
class ReportServiceProtocol(Protocol):
    """Protocol defining the interface for report generation services."""

    def generate_reports(
        self,
        config: TestSuiteConfig,
        summary: TestSuiteSummary,
    ) -> None:
        """Generate reports using the configured reporters.

        Args:
            config: Test suite configuration containing report settings
            summary: The test suite execution results to be reported
        """
        ...
