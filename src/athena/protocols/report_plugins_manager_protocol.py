from typing import Any, runtime_checkable
from typing import Protocol

from athena.models.test_suite_summary import TestSuiteSummary


@runtime_checkable
class ReportPluginsManagerProtocol(Protocol):
    """Protocol defining the interface for plugin managers."""

    def report(self, reporter_config: Any, summary: TestSuiteSummary) -> None:
        """Generate reports using the configured reporters."""
        ...
