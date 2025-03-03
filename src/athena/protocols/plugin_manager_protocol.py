from typing import Any, Optional, runtime_checkable
from typing import Protocol

from athena.models.test_config import TestConfig
from athena.models.test_result import TestResult
from athena.models.test_suite_summary import TestSuiteSummary


@runtime_checkable
class PluginManagerProtocol(Protocol):
    """Protocol defining the interface for plugin managers."""

    def parse_data(self, data: str, format: str) -> Optional[dict[str, Any]]:
        """Parse data using the appropriate parser."""
        ...

    def run_test(self, test: TestConfig) -> TestResult:
        """Run a test based on the configuration."""
        ...

    def report(self, reporter_config: Any, summary: TestSuiteSummary) -> None:
        """Generate reports using the configured reporters."""
        ...
