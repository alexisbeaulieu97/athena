from typing import Any, Dict, List

from athena.models.plugin import Plugin
from athena.models.test_config import TestConfig
from athena.models.test_result import TestResult
from athena.models.test_result_summary import TestResultSummary
from athena.models.test_suite_config import TestSuiteConfig
from athena.protocols.data_parser_service_protocol import DataParserServiceProtocol
from athena.protocols.plugin_service_protocol import PluginServiceProtocol


class TestService:
    """Component responsible for executing tests."""

    def __init__(
        self,
        plugin_service: PluginServiceProtocol[Plugin[TestResult]],
        data_parser_service: DataParserServiceProtocol,
    ) -> None:
        self.plugin_service = plugin_service
        self.data_parser_service = data_parser_service

    def run_tests(self, config: TestSuiteConfig) -> List[TestResultSummary]:
        """Execute tests based on the configuration."""
        results = []

        for test_config in config.tests:
            # Merge global parameters with test-specific ones
            merged_params = self.merge_parameters(
                config.parameters or {}, test_config.parameters or {}
            )

            # Create a new test config to avoid modifying the original
            test_config_copy = TestConfig(
                name=test_config.name,
                plugin_identifier=test_config.plugin_identifier,
                parameters=merged_params,
            )

            plugin = self.plugin_service.get_plugin(test_config.plugin_identifier)
            test_result = plugin.executor(
                plugin.parameters_model(**test_config_copy.parameters)
            )
            # test_result = plugin.executor_object.run(**test_config_copy.parameters)
            result_summary = TestResultSummary(
                config=test_config_copy, result=test_result
            )
            results.append(result_summary)

        return results

    def merge_parameters(
        self,
        global_params: Dict[str, Any],
        test_params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Merge global and test-specific parameters with proper precedence."""
        if not global_params and not test_params:
            return {}

        merged_params = {}
        if global_params:
            merged_params = global_params.copy()
        if test_params:
            merged_params.update(test_params)

        return merged_params
