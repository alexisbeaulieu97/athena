from typing import Union, Annotated
from athena.models.test_skipped_result import TestSkippedResult
from athena.models.test_passed_result import TestPassedResult
from athena.models.test_failed_result import TestFailedResult

type TestResult = Annotated[
    Union[TestSkippedResult, TestPassedResult, TestFailedResult], "TestResult"
]
