from typing import Protocol, runtime_checkable

from athena.models.plugin import Plugin


@runtime_checkable
class PluginServiceProtocol(Protocol):
    def get_plugin(self, plugin_identifier: str) -> Plugin:
        """Get a plugin by its unique idenfitier."""
        ...
