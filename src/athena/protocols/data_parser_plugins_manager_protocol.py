from typing import Any, Optional, runtime_checkable
from typing import Protocol


@runtime_checkable
class DataParserPluginsManagerProtocol(Protocol):
    """Protocol defining the interface for plugin managers."""

    def parse_data(self, data: str, format: str) -> Optional[dict[str, Any]]:
        """Parse data using the appropriate parser."""
        ...
