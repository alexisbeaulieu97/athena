from pathlib import Path

from athena.models import BaseModel
from athena.protocols.config_parser_service_protocol import ConfigParserServiceProtocol
from athena.protocols.plugin_service_protocol import PluginServiceProtocol
from athena.types import DataParserPluginResult


class ConfigParserService(ConfigParserServiceProtocol):
    """Component responsible for configuration parsing and parameter management."""

    def __init__(
        self, plugin_service: PluginServiceProtocol[DataParserPluginResult, BaseModel]
    ) -> None:
        self.plugin_service = plugin_service

    def parse(
        self,
        config: Path,
    ) -> DataParserPluginResult:
        config_raw = config.read_text()
        format_ext = config.suffix.lstrip(".")
        plugin = self.plugin_service.get_plugin(format_ext)
        return plugin.executor(
            plugin.parameters_model(
                **{
                    "data": config_raw,
                },
            )
        )
