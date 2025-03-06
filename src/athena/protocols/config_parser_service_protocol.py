from pathlib import Path
from typing import Protocol, runtime_checkable

from athena.types import DataParserPluginResult


@runtime_checkable
class ConfigParserServiceProtocol(Protocol):
    def parse(
        self,
        config: Path,
    ) -> DataParserPluginResult:
        """Parse data using the plugin service."""
        ...
