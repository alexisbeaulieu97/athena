import logging
from typing import Any, Dict, List

import pluggy

from athena.models.test_config import TestConfig
from athena.models.test_plugin import TestPlugin
from athena.models.test_result import TestResult
from athena.plugins.builtin import BUILTIN_TEST_RUNNER_PLUGINS
from athena.plugins.hookspecs import TestRunnerHooks
from athena.protocols.test_runner_protocol import TestRunnerProtocol


class TestPluginsManager:
    """Manager for test plugins."""

    def __init__(self, project_name: str) -> None:
        """Initialize the test plugins manager.

        Args:
            project_name: The name of the project
        """
        self.runners: Dict[str, TestPlugin] = {}
        self.logger = logging.getLogger(__name__)
        self.pm = pluggy.PluginManager(project_name)
        self.pm.add_hookspecs(TestRunnerHooks)

    def load_builtin_plugins(self) -> None:
        """Register essential plugins from the built-in registry."""
        for plugin in BUILTIN_TEST_RUNNER_PLUGINS:
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
        """Load all test plugins."""
        available_tests: List[TestPlugin] = self.pm.hook.register_test_plugin()
        for available_test in available_tests:
            self.runners[available_test.metadata.name] = available_test

    def get_runner(self, name: str) -> TestRunnerProtocol:
        """Get a test runner by name.

        Args:
            name: The name of the test runner

        Returns:
            The test runner protocol implementation

        Raises:
            KeyError: If the test runner doesn't exist
        """
        if name not in self.runners:
            raise KeyError(f"Test runner '{name}' not found")
        return self.runners[name].runner

    def run_test(self, test_config: TestConfig) -> TestResult:
        """Run a test based on the configuration.

        Args:
            test_config: The test configuration

        Returns:
            The test result
        """
        runner = self.get_runner(test_config.runner)
        return runner.run(**test_config.parameters)
