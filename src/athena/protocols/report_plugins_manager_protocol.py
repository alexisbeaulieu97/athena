from typing import Any, Protocol, runtime_checkable

from athena.models.test_suite_summary import TestSuiteSummary
from athena.protocols.plugins_manager_protocol import PluginsManagerProtocol


@runtime_checkable
class ReportPluginsManagerProtocol(PluginsManagerProtocol, Protocol):
    """Protocol defining the interface for plugin managers."""

    def report(self, reporter_config: Any, summary: TestSuiteSummary) -> None:
        """Generate reports using the configured reporters."""
        ...
