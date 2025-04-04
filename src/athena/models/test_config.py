from typing import Any, Dict

from pydantic import Field

from athena.models import BaseModel


class TestConfig(BaseModel):
    """Configuration for an individual test."""

    name: str
    plugin_identifier: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
