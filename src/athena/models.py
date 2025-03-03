from datetime import datetime
from enum import Enum
from typing import (
    Annotated,
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Protocol,
    TypeVar,
    Union,
    runtime_checkable,
)

from pydantic import BaseModel, Field


# Protocols for structural typing
@runtime_checkable
class ConfigParserProtocol(Protocol):
    """Protocol for configuration parsers."""

    def parse(
        self, data: str, format: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Parse a string configuration into a dictionary.

        Args:
            data: The raw configuration data as a string
            format: Optional format specifier

        Returns:
            Parsed configuration dict or None if not handled
        """
        ...


@runtime_checkable
class TestRunnerProtocol(Protocol):
    """Protocol for test runners."""

    def run(self, config: "TestConfig") -> "TestResult":
        """Run a test based on the provided configuration.

        Args:
            config: The test configuration

        Returns:
            The test result
        """
        ...


@runtime_checkable
class ReporterProtocol(Protocol):
    """Protocol for test result reporters."""

    def report(self, summary: "TestSuiteSummary") -> None:
        """Generate a report from test results.

        Args:
            summary: The test suite summary containing results
        """
        ...


# Pydantic models for data validation
class ConfigHandler(BaseModel):
    """Configuration handler metadata and implementation."""

    name: str
    version: str
    description: str
    supported_formats: List[str]
    handler: Callable[[str], dict[str, Any]]

    def get_parser(self) -> ConfigParserProtocol:
        """Create a parser that conforms to the ConfigParserProtocol."""

        handler = self.handler
        formats = self.supported_formats

        class Parser:
            def parse(
                self, data: str, format: Optional[str] = None
            ) -> Optional[Dict[str, Any]]:
                if format in formats:
                    return handler(data)
                return None

        return Parser()


class TestConfig(BaseModel):
    """Configuration for an individual test."""

    name: str
    parameters: Dict[str, Any] = Field(default_factory=dict)


class TestDetails(BaseModel):
    """Details of a test check including expected and actual values."""

    expected: Any
    actual: Any
    success: bool


class PluginMetadata(BaseModel):
    """Metadata for a plugin."""

    name: str
    version: str
    description: str


# Union type for test results
type TestResult = Annotated[
    Union["TestSkippedResult", "TestPassedResult", "TestFailedResult"], "TestResult"
]


class TestSkippedResult(BaseModel):
    """Result for a skipped test."""

    message: Optional[str] = None


class TestPassedResult(BaseModel):
    """Result for a passed test."""

    message: Optional[str] = None
    details: Optional[Dict[str, TestDetails]] = None


class TestFailedResult(BaseModel):
    """Result for a failed test."""

    message: Optional[str] = None
    details: Optional[Dict[str, TestDetails]] = None


class TestPlugin(BaseModel):
    """Test plugin with metadata and implementation."""

    metadata: PluginMetadata
    test: Callable[[dict[str, Any]], TestResult]

    def get_runner(self) -> TestRunnerProtocol:
        """Create a runner that conforms to the TestRunnerProtocol."""

        test_func = self.test

        class Runner:
            def run(self, config: TestConfig) -> TestResult:
                return test_func(config.parameters)

        return Runner()


class TestSuiteConfig(BaseModel):
    """Configuration for multiple tests."""

    tests: List[TestConfig] = Field(default_factory=list)
    parameters: Dict[str, Any] = Field(default_factory=dict)


class TestSuiteSummary(BaseModel):
    """Summary of test suite execution."""

    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    results: List[TestResult]
