from typing import Callable, Generic, Set, Type

from athena.models import BaseModel
from athena.models.plugin_metadata import PluginMetadata
from athena.types import PluginParametersType, PluginResultType


class Plugin(BaseModel, Generic[PluginResultType, PluginParametersType]):
    metadata: PluginMetadata
    executor: Callable[[PluginParametersType], PluginResultType]
    parameters_model: Type[PluginParametersType]
    identifiers: Set[str]
