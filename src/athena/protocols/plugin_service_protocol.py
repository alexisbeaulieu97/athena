from typing import Protocol, TypeVar, runtime_checkable

T = TypeVar("T", covariant=True)


@runtime_checkable
class PluginServiceProtocol(Protocol[T]):
    def get_plugin(self, plugin_identifier: str) -> T:
        """Get a plugin by its unique idenfitier."""
        ...
