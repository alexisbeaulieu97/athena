from typing import Any, Protocol, runtime_checkable

from athena.models.test_suite_summary import TestSuiteSummary


@runtime_checkable
class ReportPluginsManagerProtocol(Protocol):
    """Protocol defining the interface for plugin managers."""

    def report(self, reporter_config: Any, summary: TestSuiteSummary) -> None:
        """Generate reports using the configured reporters."""
        ...
