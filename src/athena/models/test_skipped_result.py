from typing import Optional
from athena.models import BaseModel


class TestSkippedResult(BaseModel):
    message: Optional[str] = None
