from typing import Protocol, runtime_checkable


@runtime_checkable
class PluginsManagerProtocol(Protocol):
    """Base protocol that defines the common interface for all plugin managers.

    This protocol contains the standard plugin loading methods that should be
    implemented by all plugin manager classes.
    """

    def load_builtin_plugins(self) -> None:
        """Register essential plugins from the built-in registry.

        Loads plugins that are included with the application itself.
        """
        ...

    def load_entrypoint_plugins(self, entrypoint_name: str) -> None:
        """Load plugins from setuptools entrypoints.

        Args:
            entrypoint_name: The name of the entrypoint to load plugins from.
        """
        ...

    def load_plugins(self) -> None:
        """Load all plugins.

        This method typically calls both load_builtin_plugins() and load_entrypoint_plugins()
        with appropriate parameters.
        """
        ...
