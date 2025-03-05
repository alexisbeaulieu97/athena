from pathlib import Path

from athena.protocols.plugin_service_protocol import PluginServiceProtocol
from athena.types import DataParserPluginResult


class ConfigParserService:
    """Component responsible for configuration parsing and parameter management."""

    def __init__(
        self,
        plugin_service: PluginServiceProtocol[DataParserPluginResult],
    ) -> None:
        self.plugin_service = plugin_service

    def parse(self, data: Path) -> DataParserPluginResult:
        config_raw = data.read_text()
        format_ext = data.suffix.lstrip(".")
        plugin = self.plugin_service.get_plugin(format_ext)
        return plugin.executor(
            plugin.parameters_model(
                **{
                    "data": config_raw,
                },
            )
        )
