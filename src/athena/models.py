from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class ConfigHandler(BaseModel):
    name: str
    version: str
    description: str
    supported_formats: List[str]
    handler: Callable[[str], dict[str, Any]]


class TestConfig(BaseModel):
    """Configuration for an individual test."""

    name: str
    parameters: Dict[str, Any] = Field(default_factory=dict)


class TestDetails(BaseModel):
    expected: Any
    actual: Any
    success: bool


class PluginMetadata(BaseModel):
    name: str
    version: str
    description: str


class TestResult(BaseModel):
    message: Optional[str] = None


class TestSkippedResult(TestResult): ...


class TestPassedResult(TestResult):
    details: Optional[Dict[str, TestDetails]] = None


class TestFailedResult(TestResult):
    details: Optional[Dict[str, TestDetails]] = None


class TestPlugin(BaseModel):
    metadata: PluginMetadata
    test: Callable[[dict[str, Any]], TestResult]


class TestSuiteConfig(BaseModel):
    """Configuration for multiple tests."""

    tests: List[TestConfig] = Field(default_factory=list)
    parameters: Dict[str, Any] = Field(default_factory=dict)


class TestSuiteSummary(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    results: List[TestResult]
