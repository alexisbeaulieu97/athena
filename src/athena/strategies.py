"""Test execution strategies for Athena."""

import concurrent.futures
import logging
from typing import Callable, Dict, List, Type

from athena.models import ExecutionStrategy, TestConfig, TestResult, TestFailedResult


class SequentialStrategy:
    """Executes tests one after another in sequence."""

    def execute(
        self, tests: List[TestConfig], test_runner: Callable[[TestConfig], TestResult]
    ) -> List[TestResult]:
        """Execute tests sequentially.

        Args:
            tests: List of test configurations to execute
            test_runner: Function to run individual tests

        Returns:
            List of test results in the same order as the input tests
        """
        return [test_runner(test) for test in tests]


class ParallelStrategy:
    """Executes tests in parallel using multiple worker threads."""

    def __init__(self, max_workers: int = None):
        """Initialize the parallel strategy.

        Args:
            max_workers: Maximum number of concurrent workers. If None, uses default
                         based on the system (typically CPU count).
        """
        self.max_workers = max_workers
        self.logger = logging.getLogger(__name__)

    def execute(
        self, tests: List[TestConfig], test_runner: Callable[[TestConfig], TestResult]
    ) -> List[TestResult]:
        """Execute tests in parallel.

        Args:
            tests: List of test configurations to execute
            test_runner: Function to run individual tests

        Returns:
            List of test results in the same order as the input tests
        """
        results = [None] * len(tests)
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:
            # Map tests to futures
            future_to_index = {
                executor.submit(test_runner, test): i for i, test in enumerate(tests)
            }

            # Process results as they complete
            for future in concurrent.futures.as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    results[index] = future.result()
                except Exception as e:
                    self.logger.error(f"Error executing test {tests[index].name}: {e}")
                    raise

        return results


class GroupedStrategy:
    """Executes tests in groups with dependencies between groups."""

    def __init__(self, groups: Dict[str, List[str]]):
        """Initialize the grouped strategy.

        Args:
            groups: Dictionary mapping group names to lists of test names
        """
        self.groups = groups
        self.logger = logging.getLogger(__name__)

    def execute(
        self, tests: List[TestConfig], test_runner: Callable[[TestConfig], TestResult]
    ) -> List[TestResult]:
        """Execute tests according to their defined groups.

        Tests in the same group are executed sequentially.
        Different groups can be processed in parallel if desired.

        Args:
            tests: List of test configurations to execute
            test_runner: Function to run individual tests

        Returns:
            List of test results in the same order as the input tests
        """
        # Create a map of test configs by name for easy lookup
        test_map = {test.name: test for test in tests}
        result_map = {}

        # Process each group sequentially
        for group_name, test_names in self.groups.items():
            self.logger.info(f"Executing test group: {group_name}")

            # Get the tests in this group
            group_tests = [test_map[name] for name in test_names if name in test_map]

            # Execute tests in this group sequentially
            for test in group_tests:
                result = test_runner(test)
                result_map[test.name] = result

        # Execute any tests not in groups
        ungrouped_tests = [
            test
            for test in tests
            if not any(test.name in group_tests for group_tests in self.groups.values())
        ]

        for test in ungrouped_tests:
            result = test_runner(test)
            result_map[test.name] = result

        # Return results in the same order as the input tests
        return [result_map.get(test.name) for test in tests]


class RetryStrategy:
    """Wraps another strategy and retries failed tests."""

    def __init__(self, base_strategy: ExecutionStrategy, max_retries: int = 3):
        """Initialize the retry strategy.

        Args:
            base_strategy: The underlying strategy to use for execution
            max_retries: Maximum number of retry attempts for each test
        """
        self.base_strategy = base_strategy
        self.max_retries = max_retries
        self.logger = logging.getLogger(__name__)

    def execute(
        self, tests: List[TestConfig], test_runner: Callable[[TestConfig], TestResult]
    ) -> List[TestResult]:
        """Execute tests with retry capability.

        Args:
            tests: List of test configurations to execute
            test_runner: Function to run individual tests

        Returns:
            List of test results after retries
        """

        # Function that handles retries for a single test
        def run_with_retry(test: TestConfig) -> TestResult:
            for attempt in range(self.max_retries + 1):
                result = test_runner(test)

                # If test passed or was skipped, return immediately
                if not isinstance(result, TestFailedResult):
                    return result

                # If we've reached max retries, return the last result
                if attempt == self.max_retries:
                    self.logger.warning(
                        f"Test {test.name} failed after {self.max_retries + 1} attempts"
                    )
                    return result

                self.logger.info(
                    f"Retrying test {test.name} (attempt {attempt + 1}/{self.max_retries + 1})"
                )

            # This should never be reached due to the return in the loop
            return result

        # Use the base strategy but with our retry-wrapped test runner
        return self.base_strategy.execute(tests, run_with_retry)


# Registry of available strategies
STRATEGIES: Dict[str, Type[ExecutionStrategy]] = {
    "sequential": SequentialStrategy,
    "parallel": ParallelStrategy,
}


def get_strategy(name: str, **kwargs) -> ExecutionStrategy:
    """Get a strategy by name with optional configuration.

    Args:
        name: Name of the strategy to get
        **kwargs: Additional configuration parameters for the strategy

    Returns:
        An initialized strategy instance

    Raises:
        ValueError: If the requested strategy does not exist
    """
    if name not in STRATEGIES:
        raise ValueError(f"Unknown execution strategy: {name}")

    strategy_class = STRATEGIES[name]
    return strategy_class(**kwargs)
