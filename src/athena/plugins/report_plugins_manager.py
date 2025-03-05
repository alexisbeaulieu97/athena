import logging
from typing import Dict, List

import pluggy

from athena.models.reporter_config import ReporterConfig
from athena.models.reporter_plugin import ReporterPlugin
from athena.models.test_suite_summary import TestSuiteSummary
from athena.plugins.builtin import BUILTIN_REPORTER_PLUGINS
from athena.plugins.hookspecs import ReporterHooks


class ReportPluginsManager:
    """Manager for reporter plugins."""

    def __init__(self, project_name: str) -> None:
        """Initialize the report plugins manager.

        Args:
            project_name: The name of the project
        """
        self.reporters: Dict[str, ReporterPlugin] = {}
        self.logger = logging.getLogger(__name__)
        self.pm = pluggy.PluginManager(project_name)
        self.pm.add_hookspecs(ReporterHooks)

    def load_builtin_plugins(self) -> None:
        """Register essential plugins from the built-in registry."""
        for plugin in BUILTIN_REPORTER_PLUGINS:
            self.logger.debug(f"Registering built-in plugin: {plugin.__name__}")
            self.pm.register(plugin)

    def load_entrypoint_plugins(self, entrypoint_name: str) -> None:
        """Load plugins from setuptools entrypoints."""
        try:
            self.pm.load_setuptools_entrypoints(entrypoint_name)
            self.logger.info(f"Loaded plugins from entrypoint: {entrypoint_name}")
        except Exception as e:
            self.logger.error(f"Failed to load entrypoint plugins: {e}")

    def load_plugins(self) -> None:
        """Load all reporter plugins."""
        available_reporters: List[ReporterPlugin] = (
            self.pm.hook.register_reporter_plugin()
        )
        for reporter in available_reporters:
            self.logger.debug(f"Loading reporter plugin: {reporter.metadata.name}")
            self.reporters[reporter.metadata.name] = reporter

    def get_reporter(self, name: str) -> ReporterPlugin:
        """Get a reporter by name.

        Args:
            name: The name of the reporter

        Returns:
            The reporter plugin

        Raises:
            KeyError: If the reporter doesn't exist
        """
        if name not in self.reporters:
            raise KeyError(f"Reporter '{name}' not found")
        return self.reporters[name]

    def report(
        self, reporter_config: ReporterConfig, summary: TestSuiteSummary
    ) -> None:
        """Generate a report using the specified reporter.

        Args:
            reporter_config: Configuration for the reporter
            summary: The test suite summary to report

        Raises:
            KeyError: If the specified reporter doesn't exist
        """
        if not self.reporters:
            self.logger.warning("No reporter plugins registered.")
            return

        try:
            reporter = self.get_reporter(reporter_config.name)
            reporter.reporter.report(summary, **reporter_config.parameters)
        except KeyError:
            self.logger.error(f"Reporter '{reporter_config.name}' not found.")
            raise
