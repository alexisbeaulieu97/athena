from pydantic import BaseModel
from athena.models.test_config import TestConfig
from athena.models.test_result import TestResult

class TestResultSummary(BaseModel):
    test_config: TestConfig
    test_result: TestResult
