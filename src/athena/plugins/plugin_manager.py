import logging
from typing import Any, List

import pluggy

from athena.models import (
    ConfigHandler,
    TestConfig,
    TestPlugin,
    TestResult,
    TestSkippedResult,
)
from athena.plugins import hookspecs
from athena.plugins.builtin import BUILTIN_PLUGINS


class AthenaPluginManager:
    def __init__(self) -> None:
        self.tests: dict[str, TestPlugin] = {}
        self.logger = logging.getLogger(__name__)
        self.pm = pluggy.PluginManager("athena")
        self.pm.add_hookspecs(hookspecs)
        self.load_plugins()

    @property
    def hook(self) -> pluggy.HookRelay:
        """Expose Pluggy's hook interface directly."""
        return self.pm.hook

    def load_core_plugins(self) -> None:
        """Register essential plugins from the built-in registry."""
        for plugin in BUILTIN_PLUGINS:
            self.pm.register(plugin)

    def load_entrypoint_plugins(self, entrypoint_name: str) -> None:
        """Load plugins from setuptools entrypoints."""
        try:
            self.pm.load_setuptools_entrypoints(entrypoint_name)
            self.logger.info(f"Loaded plugins from entrypoint: {entrypoint_name}")
        except Exception as e:
            self.logger.error(f"Failed to load entrypoint plugins: {e}")

    def load_plugins(self) -> None:
        """Load all plugins."""
        self.load_core_plugins()
        self.load_entrypoint_plugins("athena.plugins")
        self.load_test_plugins()

    @property
    def config_handlers(self) -> List[ConfigHandler]:
        """Get all registered configuration handlers."""
        return self.pm.hook.get_config_handler()

    def load_test_plugins(self) -> None:
        """Load all test plugins."""
        available_tests: List[TestPlugin] = self.pm.hook.register_test()
        for available_test in available_tests:
            self.tests[available_test.metadata.name] = available_test

    def run_test(self, test: TestConfig) -> TestResult:
        """Run a test based on the configuration."""
        if test.name not in self.tests:
            self.logger.warning(f"Test '{test.name}' not found.")
            return TestSkippedResult(
                message="Test not found",
            )
        return self.tests[test.name].test(test.parameters)


pm = AthenaPluginManager()
