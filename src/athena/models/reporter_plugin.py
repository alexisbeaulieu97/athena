from athena.models import BaseModel
from athena.models.plugin_metadata import PluginMetadata
from athena.protocols.reporter_protocol import ReporterProtocol


class ReporterPlugin(BaseModel):
    metadata: PluginMetadata
    reporter: ReporterProtocol
