import logging
from typing import Any, Dict, List, Optional

import pluggy

from athena.models import (
    ConfigHandler,
    ExecutionStrategy,
    TestConfig,
    TestPlugin,
    TestResult,
    TestSkippedResult,
    TestSuiteConfig,
)
from athena.plugins import hookspecs
from athena.plugins.builtin import BUILTIN_PLUGINS
from athena.strategies import get_strategy


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

    def run_test_suite(
        self,
        test_suite: TestSuiteConfig,
        strategy_name: Optional[str] = None,
        strategy_options: Optional[Dict[str, Any]] = None,
    ) -> List[TestResult]:
        """Run a suite of tests using the specified execution strategy.

        Args:
            test_suite: The test suite configuration
            strategy_name: Name of the execution strategy to use (defaults to one in config or "sequential")
            strategy_options: Additional options for the strategy

        Returns:
            List of test results
        """
        # Use the provided strategy name, or fall back to the one in config, or default to sequential
        strategy_name = strategy_name or test_suite.execution_strategy or "sequential"
        strategy_options = strategy_options or {}

        # Get the specified strategy
        try:
            strategy = get_strategy(strategy_name, **strategy_options)
        except ValueError as e:
            self.logger.warning(
                f"Invalid execution strategy '{strategy_name}', falling back to sequential: {e}"
            )
            strategy = get_strategy("sequential")

        self.logger.info(f"Running test suite using {strategy_name} strategy")

        # Create a test runner function that handles parameter merging
        def run_test_with_params(test_config: TestConfig) -> TestResult:
            # Merge global parameters with test-specific ones
            merged_params = test_suite.parameters.copy()
            merged_params.update(test_config.parameters)

            # Create a new TestConfig with the merged parameters
            merged_config = TestConfig(name=test_config.name, parameters=merged_params)

            # Run the test
            return self.run_test(merged_config)

        # Execute the tests using the selected strategy
        return strategy.execute(test_suite.tests, run_test_with_params)


pm = AthenaPluginManager()
