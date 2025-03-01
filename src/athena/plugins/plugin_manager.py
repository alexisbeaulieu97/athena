import logging
from typing import List

import pluggy

from athena.models import ConfigHandler
from athena.plugins import hookspecs
from athena.plugins.core import json_parser, yaml_parser
from athena.plugins.system_test import SystemTestPlugin


class AthenaPluginManager:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.pm = pluggy.PluginManager("athena")
        self.pm.add_hookspecs(hookspecs)
        self.load_plugins()

    @property
    def hook(self) -> pluggy.HookRelay:
        """Expose Pluggy's hook interface directly."""
        return self.pm.hook

    def load_core_plugins(self) -> None:
        """Register essential plugins (e.g., JSON/YAML handlers)."""
        core_plugins = [SystemTestPlugin(), json_parser, yaml_parser]
        for plugin in core_plugins:
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

    @property
    def config_handlers(self) -> List[ConfigHandler]:
        """Get all registered configuration handlers."""
        return self.pm.hook.get_config_handler()


pm = AthenaPluginManager()
