import json
from typing import Any

from athena.models.data_parser_plugin import DataParserPlugin
from athena.models.plugin_metadata import PluginMetadata
from athena.plugins import hookimpl


@hookimpl(tryfirst=True)
def register_data_parser_plugin() -> DataParserPlugin:
    """Register the YAML data parser plugin."""
    return DataParserPlugin(
        metadata=PluginMetadata(
            name="json",
            description="Parse JSON formatted data",
        ),
        parser=JSONDataParser(),
        supported_formats=("json",),
    )


class JSONDataParser:
    def parse(self, data: str, **kwargs: Any) -> dict[str, Any]:
        """Parse JSON formatted data."""
        return json.loads(data)
