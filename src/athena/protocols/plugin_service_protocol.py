from typing import Generic, Protocol, runtime_checkable

from athena.models.plugin import Plugin
from athena.types import PluginParametersType, PluginResultType


@runtime_checkable
class PluginServiceProtocol(Protocol, Generic[PluginResultType, PluginParametersType]):
    def get_plugin(
        self, plugin_identifier: str
    ) -> Plugin[PluginResultType, PluginParametersType]:
        """Get a plugin by its unique idenfitier."""
        ...
