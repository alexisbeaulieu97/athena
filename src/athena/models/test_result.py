from enum import Enum
from typing import Dict, Literal, Optional

from pydantic import Field

from athena.models import BaseModel
from athena.models.test_details import TestDetails


class ResultType(str, Enum):
    """Enumeration of possible test result types."""

    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


class TestResult(BaseModel):
    """Base class for all test results.

    This class represents the outcome of a test execution, including its status,
    any associated message, and optional detailed test information.

    Attributes:
        type: The result type (passed, failed, skipped)
        message: An optional message providing additional context
        details: Optional dictionary of test details, where keys are test identifiers
                and values are TestDetails objects
    """

    type: ResultType = Field(..., frozen=True)  # Make type immutable
    message: Optional[str] = None
    details: Optional[Dict[str, TestDetails]] = None

    @classmethod
    def passed(
        cls,
        message: Optional[str] = None,
        details: Optional[Dict[str, TestDetails]] = None,
    ) -> "TestResult":
        """Factory method for creating passed results.

        Args:
            message: Optional message describing why the test passed
            details: Optional dictionary containing test details

        Returns:
            A TestResult instance with type set to PASSED
        """
        return cls(type=ResultType.PASSED, message=message, details=details)

    @classmethod
    def failed(
        cls,
        message: Optional[str] = None,
        details: Optional[Dict[str, TestDetails]] = None,
    ) -> "TestResult":
        """Factory method for creating failed results.

        Args:
            message: Optional message describing why the test failed
            details: Optional dictionary containing test details

        Returns:
            A TestResult instance with type set to FAILED
        """
        return cls(type=ResultType.FAILED, message=message, details=details)

    @classmethod
    def skipped(
        cls,
        message: Optional[str] = None,
        details: Optional[Dict[str, TestDetails]] = None,
    ) -> "TestResult":
        """Factory method for creating skipped results.

        Args:
            message: Optional message describing why the test was skipped
            details: Optional dictionary containing test details

        Returns:
            A TestResult instance with type set to SKIPPED
        """
        return cls(type=ResultType.SKIPPED, message=message, details=details)

    @property
    def status(self) -> Literal["passed", "failed", "skipped"]:
        """Return a string representation of the result status.

        Returns:
            A string indicating the test result status
        """
        return self.type.value
