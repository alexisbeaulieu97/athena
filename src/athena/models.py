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


class TestStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


class TestConfig(BaseModel):
    """Configuration for an individual test."""

    name: str
    parameters: Dict[str, Any] = Field(default_factory=dict)


class TestMetadata(BaseModel):
    name: str
    version: str
    description: str


class TestSuiteConfig(BaseModel):
    """Configuration for multiple tests."""

    tests: List[TestConfig] = Field(default_factory=list)
    parameters: Dict[str, Any] = Field(default_factory=dict)


class PluginMetadata(BaseModel):
    name: str
    version: str
    description: str


class TestResult(BaseModel):
    test_name: str
    test_version: str
    duration: float
    status: TestStatus
    plugin_metadata: PluginMetadata
    message: Optional[str] = None
    details: Optional[dict[str, Any]] = None


class TestSuiteSummary(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    results: List[TestResult]

    @property
    def total_execution_time(self) -> float | Literal[0]:
        return sum(r.duration for r in self.results)

    @property
    def status_counts(self) -> Dict[str, int]:
        return {
            status: sum(1 for r in self.results if r.status == status)
            for status in TestStatus
        }
