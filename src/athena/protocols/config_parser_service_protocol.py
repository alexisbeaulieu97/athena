from pathlib import Path
from typing import Protocol, runtime_checkable

from athena.models import BaseModel
from athena.protocols.plugin_service_protocol import PluginServiceProtocol
from athena.types import DataParserPluginResult


@runtime_checkable
class ConfigParserServiceProtocol(Protocol):
    def parse(
        self,
        config: Path,
        plugin_service: PluginServiceProtocol[DataParserPluginResult, BaseModel],
    ) -> DataParserPluginResult:
        """Parse data using the plugin service."""
        ...
