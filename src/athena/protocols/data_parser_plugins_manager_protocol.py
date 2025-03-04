from typing import Any, Optional, Protocol, runtime_checkable

from athena.protocols.plugins_manager_protocol import PluginsManagerProtocol


@runtime_checkable
class DataParserPluginsManagerProtocol(PluginsManagerProtocol, Protocol):
    """Protocol defining the interface for plugin managers."""

    def parse_data(self, data: str, format: str) -> Optional[dict[str, Any]]:
        """Parse data using the appropriate parser."""
        ...
