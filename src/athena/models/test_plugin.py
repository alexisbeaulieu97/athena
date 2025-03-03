from athena.models import BaseModel
from athena.protocols.test_runner_protocol import TestRunnerProtocol
from athena.models.plugin_metadata import PluginMetadata


class TestPlugin(BaseModel):
    metadata: PluginMetadata
    runner: TestRunnerProtocol
