from athena.models import BaseModel
from athena.models.plugin_metadata import PluginMetadata
from athena.protocols.test_runner_protocol import TestRunnerProtocol


class TestPlugin(BaseModel):
    metadata: PluginMetadata
    runner: TestRunnerProtocol
