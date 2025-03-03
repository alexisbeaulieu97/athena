from typing import runtime_checkable
from typing import Protocol

from athena.models.test_config import TestConfig
from athena.models.test_result import TestResult


@runtime_checkable
class TestPluginsManagerProtocol(Protocol):
    """Protocol defining the interface for test plugin managers."""

    def run_test(self, test_config: TestConfig) -> TestResult:
        """Run a test based on the configuration."""
        ...
