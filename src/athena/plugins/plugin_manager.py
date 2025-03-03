import logging
from typing import Any, List, Optional

import pluggy


from athena.models.reporter_plugin import ReporterPlugin
from athena.models.test_suite_summary import TestSuiteSummary
from athena.plugins import hookspecs
from athena.plugins.builtin import (
    BUILTIN_PARSER_PLUGINS,
    BUILTIN_REPORTER_PLUGINS,
    BUILTIN_TEST_RUNNER_PLUGINS,
)
from athena.models.data_parser_plugin import DataParserPlugin
from athena.models.test_config import TestConfig
from athena.models.test_plugin import TestPlugin
from athena.models.test_result import TestResult
from athena.models.reporter_config import ReporterConfig


class AthenaPluginManager:
    def __init__(
        self,
        entrypoint_name: str,
        load_plugins: bool = True,
    ) -> None:
        self.parsers: dict[str, DataParserPlugin] = {}
        self.tests: dict[str, TestPlugin] = {}
        self.reporters: dict[str, ReporterPlugin] = {}
        self.logger = logging.getLogger(__name__)
        self.pm = pluggy.PluginManager("athena")
        self.pm.add_hookspecs(hookspecs)

        if load_plugins:
            self.load_all_plugins(entrypoint_name)

    @property
    def hook(self) -> pluggy.HookRelay:
        """Expose Pluggy's hook interface directly."""
        return self.pm.hook

    def load_builtin_plugins(self) -> None:
        """Register essential plugins from the built-in registry."""
        for plugin in (
            BUILTIN_PARSER_PLUGINS
            + BUILTIN_TEST_RUNNER_PLUGINS
            + BUILTIN_REPORTER_PLUGINS
        ):
            self.logger.debug(f"Registering built-in plugin: {plugin.__name__}")
            self.pm.register(plugin)

    def register_plugin(self, plugin: Any) -> None:
        """Manually register a plugin."""
        self.logger.debug(f"Manually registering plugin: {plugin.__name__}")
        self.pm.register(plugin)

    def load_entrypoint_plugins(self, entrypoint_name: str) -> None:
        """Load plugins from setuptools entrypoints."""
        try:
            self.pm.load_setuptools_entrypoints(entrypoint_name)
            self.logger.info(f"Loaded plugins from entrypoint: {entrypoint_name}")
        except Exception as e:
            self.logger.error(f"Failed to load entrypoint plugins: {e}")

    def load_all_plugins(self, entrypoint_name: str) -> None:
        """Load all plugins."""
        self.logger.info("Loading all plugins")
        self.load_builtin_plugins()
        self.load_entrypoint_plugins(entrypoint_name)
        self.load_test_runner_plugins()
        self.load_data_parser_plugins()
        self.load_reporter_plugins()

    def load_test_runner_plugins(self) -> None:
        """Load all test plugins."""
        available_tests: List[TestPlugin] = self.pm.hook.register_test_plugin()
        for available_test in available_tests:
            self.tests[available_test.metadata.name] = available_test

    def run_test(self, test: TestConfig) -> TestResult:
        """Run a test based on the configuration."""
        if test.name not in self.tests:
            self.logger.warning(f"Test '{test.name}' not found.")
            return TestResult.skipped(
                message="Test not found",
            )
        return self.tests[test.name].runner.run(
            **test.parameters if test.parameters else {}
        )

    def load_data_parser_plugins(self) -> None:
        """Load all data parsers."""
        parsers: List[DataParserPlugin] = self.pm.hook.register_data_parser_plugin()
        for parser in parsers:
            self.logger.debug(
                f'Loading data parser "{parser.metadata.name}" for supported formats "{parser.supported_formats}"'
            )
            for ext in parser.supported_formats:
                self.parsers[ext] = parser

    def parse_data(self, data: str, format: str) -> Optional[dict[str, Any]]:
        """Parse data using the appropriate parser."""
        if format not in self.parsers:
            self.logger.warning(f"No parser found for format '{format}'")
            return None
        return self.parsers[format].parser.parse(data)

    def load_reporter_plugins(self) -> None:
        """Load all reporter plugins."""
        reporters: List[ReporterPlugin] = self.pm.hook.register_reporter_plugin()
        for reporter in reporters:
            self.logger.debug(f"Loading reporter plugin: {reporter.metadata.name}")
            self.reporters[reporter.metadata.name] = reporter

    def report(
        self,
        reporter_config: ReporterConfig,
        summary: TestSuiteSummary,
    ) -> None:
        """Report using all available reporters."""
        if not self.reporters:
            self.logger.warning("No reporter plugins registered.")
            return
        self.reporters[reporter_config.name].reporter.report(summary)
