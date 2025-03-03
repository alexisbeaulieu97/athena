from typing import List

import typer
from athena.managers.configuration_manager import ConfigurationManager
from athena.models.athena_test_suite_config import AthenaTestSuiteConfig
from athena.models.test_config import TestConfig
from athena.models.test_result import TestResult
from athena.protocols.plugin_manager_protocol import PluginManagerProtocol


class TestExecutor:
    """Component responsible for executing tests."""

    def __init__(
        self,
        plugin_manager: PluginManagerProtocol,
        config_manager: ConfigurationManager,
    ) -> None:
        self.plugin_manager = plugin_manager
        self.config_manager = config_manager

    def run_tests(self, config: AthenaTestSuiteConfig) -> List[TestResult]:
        """Execute tests based on the configuration."""
        results = []

        for test_config in config.tests:
            # Merge global parameters with test-specific ones
            merged_params = self.config_manager.merge_parameters(
                config.parameters or {}, test_config.parameters or {}
            )

            # Create a new test config to avoid modifying the original
            test_config_copy = TestConfig(
                name=test_config.name, parameters=merged_params
            )

            result = self.plugin_manager.run_test(test_config_copy)
            results.append(result)
            # TODO move this to main CLI
            typer.echo(result)

        return results
