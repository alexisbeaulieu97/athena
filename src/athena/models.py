from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class TestStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


class TestResult(BaseModel):
    plugin_name: str
    test_name: str
    test_version: str
    duration: float
    status: TestStatus
    message: Optional[str] = None
    details: Optional[dict[str, Any]] = None


class TestSummary(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    execution_time: float
    results: List[TestResult]
    summary: Dict[str, int] = Field(default_factory=dict)

    def __init__(self, **data):
        if 'execution_time' not in data:
            data['execution_time'] = sum(r.duration for r in data.get('results', []))
        if 'summary' not in data:
            results = data.get('results', [])
            data['summary'] = {
                "success": sum(1 for r in results if r.status == TestStatus.SUCCESS),
                "failed": sum(1 for r in results if r.status == TestStatus.FAILED),
                "skipped": sum(1 for r in results if r.status == TestStatus.SKIPPED),
                "error": sum(1 for r in results if r.status == TestStatus.ERROR),
            }
        super().__init__(**data)
