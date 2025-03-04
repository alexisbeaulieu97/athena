from typing import Any, Dict, Optional

from pydantic import Field

from athena.models import BaseModel


class ReporterConfig(BaseModel):
    name: str
    parameters: Optional[Dict[str, Any]] = Field(default_factory=dict)
