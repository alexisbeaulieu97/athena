from typing import Any, Optional, Protocol, runtime_checkable


@runtime_checkable
class DataParserPluginsManagerProtocol(Protocol):
    """Protocol defining the interface for plugin managers."""

    def parse_data(self, data: str, format: str) -> Optional[dict[str, Any]]:
        """Parse data using the appropriate parser."""
        ...
