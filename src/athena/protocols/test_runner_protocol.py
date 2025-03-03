from typing import Any
from typing_extensions import Protocol, runtime_checkable
from athena.models.test_result import TestResult


@runtime_checkable
class TestRunnerProtocol(Protocol):
    """Protocol for test runners."""

    def run(self, **kwargs: Any) -> TestResult:
        """Run a test based on the provided configuration.

        Returns:
            The test result
        """
        ...
