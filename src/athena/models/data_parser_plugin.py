from typing import Iterable

from athena.models import BaseModel
from athena.models.plugin_metadata import PluginMetadata
from athena.protocols.data_parser_protocol import DataParserProtocol


class DataParserPlugin(BaseModel):
    metadata: PluginMetadata
    parser: DataParserProtocol
    supported_formats: Iterable[str]
