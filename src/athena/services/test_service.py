from typing import List

from athena.models.athena_test_suite_config import AthenaTestSuiteConfig
from athena.models.test_config import TestConfig
from athena.models.test_result_summary import TestResultSummary
from athena.protocols.test_plugins_manager_protocol import TestPluginsManagerProtocol
from athena.services.configuration_service import ConfigurationService


class TestService:
    """Component responsible for executing tests."""

    def __init__(
        self,
        plugin_manager: TestPluginsManagerProtocol,
        config_manager: ConfigurationService,
    ) -> None:
        self.plugin_manager = plugin_manager
        self.config_manager = config_manager

    def run_tests(self, config: AthenaTestSuiteConfig) -> List[TestResultSummary]:
        """Execute tests based on the configuration."""
        results = []

        for test_config in config.tests:
            # Merge global parameters with test-specific ones
            merged_params = self.config_manager.merge_parameters(
                config.parameters or {}, test_config.parameters or {}
            )

            # Create a new test config to avoid modifying the original
            test_config_copy = TestConfig(
                name=test_config.name,
                runner=test_config.runner,
                parameters=merged_params,
            )

            test_result = self.plugin_manager.run_test(test_config_copy)
            result_summary = TestResultSummary(
                config=test_config_copy, result=test_result
            )
            results.append(result_summary)

        return results
