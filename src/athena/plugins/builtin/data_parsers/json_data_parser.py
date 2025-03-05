import json
from typing import Any

from athena.models.plugin import Plugin
from athena.models.plugin_metadata import PluginMetadata
from athena.plugins import hookimpl
from athena.protocols.data_parser_protocol import DataParserProtocol


@hookimpl
def activate_data_parser_plugin() -> Plugin[DataParserProtocol]:
    """Register the YAML data parser plugin."""
    return Plugin(
        metadata=PluginMetadata(
            name="json",
            description="Parse JSON formatted data",
        ),
        executor=JSONDataParser(),
        identifiers=("json",),
    )


class JSONDataParser:
    def parse(self, data: str, **kwargs: Any) -> dict[str, Any]:
        """Parse JSON formatted data."""
        return json.loads(data)
