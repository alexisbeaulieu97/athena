from typing import Any

import yaml

from athena.models.plugin import Plugin
from athena.models.plugin_metadata import PluginMetadata
from athena.plugins import hookimpl
from athena.protocols.data_parser_protocol import DataParserProtocol


@hookimpl
def activate_data_parser_plugin() -> Plugin[DataParserProtocol]:
    """Register the YAML data parser plugin."""
    return Plugin(
        metadata=PluginMetadata(
            name="yaml",
            description="Parse YAML formatted data",
        ),
        executor=YAMLDataParser(),
        identifiers=("yaml", "yml"),
    )


class YAMLDataParser:
    def parse(self, data: str, **kwargs: Any) -> dict[str, Any]:
        """Parse YAML formatted data."""
        return yaml.safe_load(data)
