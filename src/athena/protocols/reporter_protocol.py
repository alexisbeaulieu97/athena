from typing import Any

from typing_extensions import Protocol, runtime_checkable

from athena.models.test_suite_summary import TestSuiteSummary


@runtime_checkable
class ReporterProtocol(Protocol):
    """Protocol for test result reporters."""

    def report(self, summary: TestSuiteSummary) -> None:
        """Generate a report from test results.

        Args:
            summary: The test suite summary containing results
        """
        ...
