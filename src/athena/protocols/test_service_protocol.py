from typing import List, Protocol, runtime_checkable

from athena.models.test_result_summary import TestResultSummary
from athena.models.test_suite_config import TestSuiteConfig


@runtime_checkable
class TestServiceProtocol(Protocol):
    """Protocol defining the interface for test execution services."""

    def run_tests(self, config: TestSuiteConfig) -> List[TestResultSummary]:
        """Execute tests based on the configuration.

        Args:
            config: Test suite configuration containing test definitions

        Returns:
            List of test execution result summaries
        """
        ...
