import time
from typing import Any, Optional

import pluggy

from athena.models import TestConfig, TestsConfig, TestSummary
from athena.plugins import hookspecs
from athena.plugins.json_plugin import JsonConfigHandler
from athena.plugins.system_test import SystemTestPlugin
from athena.plugins.yaml_plugin import YamlConfigHandler


class PluginManager:
    def __init__(self):
        self.pm = pluggy.PluginManager("athena")
        self.pm.add_hookspecs(hookspecs)
        self.load_plugins()

    def load_plugins(self):
        # Register handlers
        handlers = [
            JsonConfigHandler(),
            YamlConfigHandler(),
        ]
        for handler in handlers:
            self.pm.register(handler)

        # Register test plugins
        test_plugins = [SystemTestPlugin()]
        for plugin in test_plugins:
            metadata = plugin.athena_register_test()
            # Could add validation/dependency checking here
            self.pm.register(plugin)

        self.pm.load_setuptools_entrypoints("athena.plugins")

    def import_config(self, config: str, format: Optional[str] = None) -> Optional[dict[str, Any]]:
        return self.pm.hook.athena_import_config(config=config, format=format)

    def _parse_test_configs(self, config: dict[str, Any]) -> TestsConfig:
        """Parse the raw config dict into a structured TestsConfig object."""
        if "tests" not in config:
            return TestsConfig()

        tests_list = []
        for test_config in config.get("tests", []):
            if isinstance(test_config, dict):
                test_name = test_config.get("name")
                if test_name:
                    parameters = test_config.get("parameters", {})
                    tests_list.append(TestConfig(name=test_name, parameters=parameters))

        global_params = {k: v for k, v in config.items() if k != "tests"}
        return TestsConfig(tests=tests_list, global_parameters=global_params)

    def run_test(self, config: dict[str, Any]) -> TestSummary:
        results = []
        start_time = time.time()

        # Parse config into structured format
        tests_config = self._parse_test_configs(config)

        # Get all registered test plugins
        test_plugins = [p for p in self.pm.get_plugins() if hasattr(p, 'athena_register_test')]

        # Run each configured test
        for test_config in tests_config.tests:
            # Merge global parameters with test-specific parameters
            # Test-specific parameters take precedence
            test_params = {**tests_config.global_parameters, **test_config.parameters}

            # Run the test across all plugins
            for plugin in test_plugins:
                result = self.pm.hook.athena_run_test(name=test_config.name, config=test_params)
                if result:
                    results.extend(result)

        return TestSummary(
            results=results,
            execution_time=time.time() - start_time
        )

    def export_config(self, config: dict[str, Any], format: Optional[str] = None) -> Optional[str]:
        return self.pm.hook.athena_export_config(config=config, format=format)

    def handle_report(self, summary: TestSummary) -> None:
        self.pm.hook.athena_handle_report(summary=summary)
