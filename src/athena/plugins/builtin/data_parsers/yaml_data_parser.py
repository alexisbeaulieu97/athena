from typing import Any
from athena.models.data_parser_plugin import DataParserPlugin
from athena.models.plugin_metadata import PluginMetadata
from athena.plugins import hookimpl
import yaml


@hookimpl(tryfirst=True)
def register_data_parser_plugin() -> DataParserPlugin:
    """Register the YAML data parser plugin."""
    return DataParserPlugin(
        metadata=PluginMetadata(
            name="yaml",
            description="Parse YAML formatted data",
        ),
        parser=YAMLDataParser(),
        supported_formats=("yaml", "yml"),
    )


class YAMLDataParser:
    def parse(self, data: str, **kwargs: Any) -> dict[str, Any]:
        """Parse YAML formatted data."""
        return yaml.safe_load(data)
