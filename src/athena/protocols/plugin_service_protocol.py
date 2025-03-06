from typing import Generic, List, Protocol, runtime_checkable

from athena.models.plugin import Plugin
from athena.types import PluginParametersType, PluginResultType


@runtime_checkable
class PluginServiceProtocol(Protocol, Generic[PluginResultType, PluginParametersType]):
    def register_plugin(
        self, plugin: Plugin[PluginResultType, PluginParametersType]
    ) -> None:
        """Register a plugin."""
        ...

    def register_plugins(
        self, plugins: List[Plugin[PluginResultType, PluginParametersType]]
    ) -> None:
        """Register multiple plugins."""
        ...

    def get_plugin(
        self, plugin_identifier: str
    ) -> Plugin[PluginResultType, PluginParametersType]:
        """Get a plugin by its unique idenfitier."""
        ...
