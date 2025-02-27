import time
from typing import Any, Optional

import pluggy

from athena.models import TestSummary
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

    def run_test(self, config: dict[str, Any]) -> TestSummary:
        results = []
        start_time = time.time()

        # Get all registered test plugins
        test_plugins = [p for p in self.pm.get_plugins() if hasattr(p, 'athena_register_test')]

        # Run each test from each plugin
        for plugin in test_plugins:
            metadata = plugin.athena_register_test()
            # Here we could get available tests from plugin metadata
            # For now, hardcoding known test names
            for test_name in ["system_info", "memory_check"]:
                result = self.pm.hook.athena_run_test(name=test_name, config=config)
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
