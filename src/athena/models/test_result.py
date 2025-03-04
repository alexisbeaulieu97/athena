from enum import Enum
from typing import Dict, Optional

from pydantic import Field

from athena.models import BaseModel
from athena.models.test_details import TestDetails


class ResultType(str, Enum):
    """Enumeration of possible test result types."""

    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


class TestResult(BaseModel):
    """Base class for all test results."""

    type: ResultType = Field(..., frozen=True)  # Make type immutable
    message: Optional[str] = None
    details: Optional[Dict[str, TestDetails]] = None

    @classmethod
    def passed(
        cls,
        message: Optional[str] = None,
        details: Optional[Dict[str, TestDetails]] = None,
    ) -> "TestResult":
        """Factory method for creating passed results."""
        return cls(type=ResultType.PASSED, message=message, details=details)

    @classmethod
    def failed(
        cls,
        message: Optional[str] = None,
        details: Optional[Dict[str, TestDetails]] = None,
    ) -> "TestResult":
        """Factory method for creating failed results."""
        return cls(type=ResultType.FAILED, message=message, details=details)

    @classmethod
    def skipped(cls, message: Optional[str] = None) -> "TestResult":
        """Factory method for creating skipped results."""
        return cls(type=ResultType.SKIPPED, message=message)

    @property
    def status(self) -> str:
        """Return a string representation of the result status."""
        return self.type.value
