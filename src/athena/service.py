"""Service layer for Athena.

This module provides the core services for Athena, including:
- TestService: Central service for running tests and managing test-related operations
- PluginService: Service for managing plugins and their lifecycle
- ConfigService: Service for handling configuration operations

These services use the Protocol-based interfaces to interact with plugins.
"""

import logging
from typing import Any, Dict, List, Optional, Type, Union

from athena.interfaces import (
    CompositeParser,
    CompositeReporter,
    PluginAdapter,
    PluginProviderProtocol,
)
from athena.models import (
    ConfigParserProtocol,
    ReporterProtocol,
    TestConfig,
    TestResult,
    TestRunnerProtocol,
    TestSuiteConfig,
    TestSuiteSummary,
)


class PluginService:
    """Service for managing plugins."""

    def __init__(self):
        """Initialize the plugin service."""
        self.providers: List[PluginProviderProtocol] = []
        self.parsers: List[ConfigParserProtocol] = []
        self.runners: Dict[str, TestRunnerProtocol] = {}
        self.reporters: List[ReporterProtocol] = []
        self.logger = logging.getLogger(__name__)

    def register_provider(self, provider: PluginProviderProtocol) -> None:
        """Register a plugin provider.

        Args:
            provider: A plugin provider that conforms to PluginProviderProtocol
        """
        self.providers.append(provider)

        # Register parsers, runners, and reporters from the provider
        self.parsers.extend(provider.get_parsers())

        # Register runners, handling conflicts
        for name, runner in provider.get_runners().items():
            if name in self.runners:
                self.logger.warning(f"Replacing existing runner for '{name}'")
            self.runners[name] = runner

        self.reporters.extend(provider.get_reporters())

    def register_plugin(self, plugin: Any) -> None:
        """Register a plugin via an adapter.

        Args:
            plugin: A plugin object that implements hook methods
        """
        adapter = PluginAdapter(plugin)
        self.register_provider(adapter)

    def get_parser(self) -> ConfigParserProtocol:
        """Get a composite parser that tries all registered parsers.

        Returns:
            A composite parser
        """
        return CompositeParser(self.parsers)

    def get_reporter(self) -> ReporterProtocol:
        """Get a composite reporter that calls all registered reporters.

        Returns:
            A composite reporter
        """
        return CompositeReporter(self.reporters)

    def get_runner(self, name: str) -> Optional[TestRunnerProtocol]:
        """Get a test runner by name.

        Args:
            name: The name of the test runner to get

        Returns:
            The test runner or None if not found
        """
        return self.runners.get(name)


class ConfigService:
    """Service for handling configuration operations."""

    def __init__(self, plugin_service: PluginService):
        """Initialize the configuration service.

        Args:
            plugin_service: The plugin service to use for parsing
        """
        self.plugin_service = plugin_service
        self.logger = logging.getLogger(__name__)

    def parse_config(
        self, data: str, format: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Parse a configuration string.

        Args:
            data: The raw configuration data as a string
            format: Optional format specifier

        Returns:
            Parsed configuration dict or None if parsing failed
        """
        parser = self.plugin_service.get_parser()
        return parser.parse(data, format)

    def build_test_suite(self, config: Dict[str, Any]) -> TestSuiteConfig:
        """Build a test suite configuration from a parsed configuration.

        Args:
            config: The parsed configuration

        Returns:
            A test suite configuration
        """
        # Extract tests
        test_configs = []
        for test_dict in config.get("tests", []):
            test_configs.append(TestConfig(**test_dict))

        # Create test suite config
        return TestSuiteConfig(
            tests=test_configs,
            parameters=config.get("parameters", {}),
        )


class TestService:
    """Service for running tests and managing test-related operations."""

    def __init__(self, plugin_service: PluginService):
        """Initialize the test service.

        Args:
            plugin_service: The plugin service to use for test operations
        """
        self.plugin_service = plugin_service
        self.logger = logging.getLogger(__name__)

    def run_test(self, config: TestConfig) -> TestResult:
        """Run a single test.

        Args:
            config: The test configuration

        Returns:
            The test result
        """
        # Get the runner for this test
        runner = self.plugin_service.get_runner(config.name)

        # If no runner is found, return a skipped result
        if runner is None:
            self.logger.warning(f"No runner found for test '{config.name}'")
            from athena.models import TestSkippedResult

            return TestSkippedResult(
                message=f"No runner found for test '{config.name}'"
            )

        # Run the test
        return runner.run(config)

    def run_test_suite(self, suite: TestSuiteConfig) -> TestSuiteSummary:
        """Run a test suite.

        Args:
            suite: The test suite configuration

        Returns:
            A summary of the test suite execution
        """
        # Run all tests in the suite
        results = []
        for test_config in suite.tests:
            # Create a new test config with merged parameters
            merged_params = suite.parameters.copy()
            merged_params.update(test_config.parameters)
            merged_config = TestConfig(
                name=test_config.name,
                parameters=merged_params,
            )

            # Run the test and collect the result
            result = self.run_test(merged_config)
            results.append(result)

        # Create a summary
        summary = TestSuiteSummary(results=results)

        # Generate reports
        reporter = self.plugin_service.get_reporter()
        reporter.report(summary)

        return summary
