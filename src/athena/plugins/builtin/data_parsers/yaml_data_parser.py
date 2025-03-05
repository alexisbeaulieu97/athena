import yaml

from athena.models import BaseModel
from athena.models.plugin import Plugin
from athena.models.plugin_metadata import PluginMetadata
from athena.plugins import hookimpl
from athena.types import DataParserPluginResult


class YAMLDataParserParameters(BaseModel):
    data: str


@hookimpl
def activate_data_parser_plugin() -> Plugin[
    DataParserPluginResult,
    YAMLDataParserParameters,
]:
    """Register the YAML data parser plugin."""
    return Plugin(
        metadata=PluginMetadata(
            name="yaml",
            description="Parse YAML formatted data",
        ),
        executor=YAMLDataParser(),
        parameters_model=YAMLDataParserParameters,
        identifiers={"yaml", "yml"},
    )


class YAMLDataParser:
    def __call__(self, parameters: YAMLDataParserParameters) -> DataParserPluginResult:
        return yaml.safe_load(parameters.data)
