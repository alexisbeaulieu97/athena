from datetime import datetime
from typing import List

from pydantic import Field

from athena.models import BaseModel
from athena.models.test_result import TestResult


class TestSuiteSummary(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    results: List[TestResult]
