from typing import Dict, List, TypeVar

from athena.models.plugin import Plugin
from athena.protocols.plugin_service_protocol import PluginServiceProtocol

PluginType = TypeVar("PluginType", bound=Plugin)


class PluginService(PluginServiceProtocol[PluginType]):
    def __init__(self) -> None:
        self.plugin_registry: Dict[str, PluginType] = {}

    def register_plugin(self, plugin: PluginType) -> None:
        """Register a plugin with the service.

        Args:
            plugin: The plugin to register

        Raises:
            ValueError: If a plugin with any of the same identifiers is already registered
        """
        for identifier in plugin.identifiers:
            if identifier in self.plugin_registry:
                raise ValueError(
                    f"Plugin with identifier '{identifier}' already registered"
                )
            self.plugin_registry[identifier] = plugin

    def register_plugins(self, plugins: List[PluginType]) -> None:
        """Register multiple plugins with the service.

        Args:
            plugins: A list of plugins to register

        Raises:
            ValueError: If any plugin has an identifier that is already registered
        """
        for plugin in plugins:
            self.register_plugin(plugin)

    def get_plugin(self, plugin_identifier: str) -> PluginType:
        """Get a plugin by its unique identifier.

        Args:
            plugin_identifier: The unique identifier of the plugin

        Returns:
            The plugin with the specified identifier

        Raises:
            KeyError: If no plugin with the specified identifier exists
        """
        if plugin_identifier not in self.plugin_registry:
            raise KeyError(f"Plugin '{plugin_identifier}' not found")
        return self.plugin_registry[plugin_identifier]
