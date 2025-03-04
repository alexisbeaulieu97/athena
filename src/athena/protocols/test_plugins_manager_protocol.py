from typing import Protocol, runtime_checkable

from athena.models.test_config import TestConfig
from athena.models.test_result import TestResult
from athena.protocols.plugins_manager_protocol import PluginsManagerProtocol


@runtime_checkable
class TestPluginsManagerProtocol(PluginsManagerProtocol, Protocol):
    """Protocol defining the interface for test plugin managers."""

    def run_test(self, test_config: TestConfig) -> TestResult:
        """Run a test based on the configuration."""
        ...
