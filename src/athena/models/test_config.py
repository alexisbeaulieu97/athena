from typing import Any, Dict, Optional
from athena.models import BaseModel
from pydantic import Field


class TestConfig(BaseModel):
    """Configuration for an individual test."""

    name: str
    parameters: Optional[Dict[str, Any]] = Field(default_factory=dict)
