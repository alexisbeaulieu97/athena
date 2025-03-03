from typing import Any, Dict
from athena.models import BaseModel
from pydantic import Field


class TestConfig(BaseModel):
    """Configuration for an individual test."""

    name: str
    runner: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
