# from typing import Any, Callable, Dict, Iterable, List, Optional
# from athena.models import BaseModel, Field
# from athena.types import TestResult, TestDetails, TestSuiteSummary
# from athena.protocols import DataParserProtocol, TestRunnerProtocol, ReporterProtocol


# class ConfigHandler(BaseModel):
#     name: str
#     version: str
#     description: str
#     supported_formats: List[str]
#     handler: Callable[[str], dict[str, Any]]


# class TestSuiteConfig(BaseModel):
#     """Configuration for multiple tests."""

#     tests: List[TestConfig] = Field(default_factory=list)
#     parameters: Dict[str, Any] = Field(default_factory=dict)
