from abc import ABC, abstractmethod
from typing import Any, Optional, Protocol

from athena.plugins import hookimpl


class ConfigHandler(Protocol):
    """Base class for config handlers that can import and export."""

    format: str

    @hookimpl
    def athena_import_config(self, config: str, format: Optional[str] = None) -> Optional[dict[str, Any]]:
        """Import config from a string."""
        if format is not None and format != self.format:
            return None
        return self._import_config(config)

    @hookimpl
    def athena_export_config(self, config: dict[str, Any], format: Optional[str] = None) -> Optional[str]:
        """Export config to a string."""
        if format is not None and format != self.format:
            return None
        return self._export_config(config)

    @abstractmethod
    def _import_config(self, config: str) -> Optional[dict[str, Any]]:
        """Implementation of the config import."""
        pass

    @abstractmethod
    def _export_config(self, config: dict[str, Any]) -> Optional[str]:
        """Implementation of the config export."""
        pass
