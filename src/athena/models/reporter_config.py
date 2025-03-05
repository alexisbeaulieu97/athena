from typing import Any, Dict

from pydantic import Field

from athena.models import BaseModel


class ReporterConfig(BaseModel):
    name: str
    plugin_identifier: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
