from pydantic import Field
from athena.models import BaseModel
from typing import Any, Dict, Optional


class ReporterConfig(BaseModel):
    name: str
    parameters: Optional[Dict[str, Any]] = Field(default_factory=dict)
