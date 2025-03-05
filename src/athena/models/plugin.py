from typing import Generic, Iterable, TypeVar

from athena.models import BaseModel
from athena.models.plugin_metadata import PluginMetadata

ExecutorType = TypeVar("ExecutorType", covariant=True)


class Plugin(BaseModel, Generic[ExecutorType]):
    metadata: PluginMetadata
    executor: ExecutorType
    identifiers: Iterable[str]
