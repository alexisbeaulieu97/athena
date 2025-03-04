from typing import Any

from athena.models import BaseModel


class TestDetails(BaseModel):
    expected: Any
    actual: Any
    success: bool
