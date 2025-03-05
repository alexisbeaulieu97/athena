import json

from athena.models import BaseModel
from athena.models.plugin import Plugin
from athena.models.plugin_metadata import PluginMetadata
from athena.plugins import hookimpl
from athena.types import DataParserPluginResult


class JSONDataParserParameters(BaseModel):
    data: str


@hookimpl
def activate_data_parser_plugin() -> Plugin[
    DataParserPluginResult,
    JSONDataParserParameters,
]:
    """Register the YAML data parser plugin."""
    return Plugin(
        metadata=PluginMetadata(
            name="json",
            description="Parse JSON formatted data",
        ),
        executor=JSONDataParser(),
        parameters_model=JSONDataParserParameters,
        identifiers={"json"},
    )


class JSONDataParser:
    def __call__(self, parameters: JSONDataParserParameters) -> DataParserPluginResult:
        return json.loads(parameters.data)
