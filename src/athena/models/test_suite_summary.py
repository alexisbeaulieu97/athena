from datetime import datetime
from typing import List
from athena.models import BaseModel
from athena.models.test_result import TestResult
from pydantic import Field


class TestSuiteSummary(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    results: List[TestResult]
