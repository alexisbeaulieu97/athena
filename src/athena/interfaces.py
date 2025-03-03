"""Interfaces for Athena plugins and adapters.

This module provides interfaces and adapters for extending Athena with custom plugins.
It uses Protocol classes for structural typing, allowing for more flexible plugin development.
"""

from typing import Any, Dict, List, Optional, Protocol, Type, runtime_checkable

from athena.models import (
    ConfigParserProtocol,
    ReporterProtocol,
    TestConfig,
    TestResult,
    TestRunnerProtocol,
    TestSuiteSummary,
)


@runtime_checkable
class PluginProviderProtocol(Protocol):
    """Protocol for plugin providers.

    Plugin providers are responsible for creating and managing plugins.
    They can be used to create parsers, runners, and reporters.
    """

    def get_parsers(self) -> List[ConfigParserProtocol]:
        """Get the configuration parsers provided by this provider."""
        ...

    def get_runners(self) -> Dict[str, TestRunnerProtocol]:
        """Get the test runners provided by this provider."""
        ...

    def get_reporters(self) -> List[ReporterProtocol]:
        """Get the reporters provided by this provider."""
        ...


class PluginAdapter:
    """Adapter for using plugins with the Protocol-based interfaces.

    This adapter converts existing hooks-based plugins to the Protocol-based interfaces.
    """

    def __init__(self, plugin: Any):
        """Initialize the adapter with a plugin.

        Args:
            plugin: A plugin object that implements hook methods
        """
        self.plugin = plugin

    def get_parsers(self) -> List[ConfigParserProtocol]:
        """Get config parsers from the plugin.

        This converts the parse_raw_data hook to ConfigParserProtocol objects.

        Returns:
            List of parser objects conforming to ConfigParserProtocol
        """
        parsers = []

        # Check if the plugin has a parse_raw_data method
        if hasattr(self.plugin, "parse_raw_data"):
            # Create a parser that wraps the plugin's parse_raw_data method
            class PluginParser:
                def __init__(self, parse_func):
                    self.parse_func = parse_func

                def parse(
                    self, data: str, format: Optional[str] = None
                ) -> Optional[Dict[str, Any]]:
                    return self.parse_func(data=data, format=format)

            parsers.append(PluginParser(self.plugin.parse_raw_data))

        return parsers

    def get_runners(self) -> Dict[str, TestRunnerProtocol]:
        """Get test runners from the plugin.

        This converts test functions registered via the register_test hook to TestRunnerProtocol objects.

        Returns:
            Dictionary mapping test names to runner objects conforming to TestRunnerProtocol
        """
        runners = {}

        # Check if the plugin has a register_test method
        if hasattr(self.plugin, "register_test"):
            # Get test plugins from the register_test method
            test_plugins = self.plugin.register_test()

            # Convert each test plugin to a runner
            for test_plugin in test_plugins:
                # Create a runner that wraps the test plugin's test function
                class PluginRunner:
                    def __init__(self, test_func):
                        self.test_func = test_func

                    def run(self, config: TestConfig) -> TestResult:
                        return self.test_func(config.parameters)

                runners[test_plugin.metadata.name] = PluginRunner(test_plugin.test)

        return runners

    def get_reporters(self) -> List[ReporterProtocol]:
        """Get reporters from the plugin.

        This converts the handle_report hook to ReporterProtocol objects.

        Returns:
            List of reporter objects conforming to ReporterProtocol
        """
        reporters = []

        # Check if the plugin has a handle_report method
        if hasattr(self.plugin, "handle_report"):
            # Create a reporter that wraps the plugin's handle_report method
            class PluginReporter:
                def __init__(self, report_func):
                    self.report_func = report_func

                def report(self, summary: TestSuiteSummary) -> None:
                    self.report_func(summary=summary)

            reporters.append(PluginReporter(self.plugin.handle_report))

        return reporters


class CompositeParser(ConfigParserProtocol):
    """A composite parser that delegates to multiple parsers.

    This parser tries each parser in sequence until one returns a non-None result.
    """

    def __init__(self, parsers: List[ConfigParserProtocol]):
        """Initialize the composite parser with a list of parsers.

        Args:
            parsers: List of parsers to delegate to
        """
        self.parsers = parsers

    def parse(
        self, data: str, format: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Parse data using the first parser that returns a non-None result.

        Args:
            data: The raw configuration data as a string
            format: Optional format specifier

        Returns:
            Parsed configuration dict or None if no parser handled the data
        """
        for parser in self.parsers:
            result = parser.parse(data, format)
            if result is not None:
                return result
        return None


class CompositeReporter(ReporterProtocol):
    """A composite reporter that delegates to multiple reporters.

    This reporter calls all reporters in sequence.
    """

    def __init__(self, reporters: List[ReporterProtocol]):
        """Initialize the composite reporter with a list of reporters.

        Args:
            reporters: List of reporters to delegate to
        """
        self.reporters = reporters

    def report(self, summary: TestSuiteSummary) -> None:
        """Generate reports using all reporters.

        Args:
            summary: The test suite summary containing results
        """
        for reporter in self.reporters:
            reporter.report(summary)
