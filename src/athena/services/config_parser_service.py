from pathlib import Path
from typing import Any, Dict

from athena.models.plugin import Plugin
from athena.protocols.data_parser_service_protocol import DataParserServiceProtocol
from athena.protocols.plugin_service_protocol import PluginServiceProtocol


class ConfigParserService(DataParserServiceProtocol[Path, Dict[str, Any]]):
    """Component responsible for configuration parsing and parameter management."""

    def __init__(
        self,
        plugin_service: PluginServiceProtocol,
    ) -> None:
        self.plugin_service = plugin_service

    def parse_data(self, data: Path) -> Dict[str, Any]:
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
