from typing import Any, Dict, Optional, TypeVar

from athena.models import BaseModel
from athena.models.test_result import TestResult

DataParserPluginResult = Dict[str, Any]
TestRunnerPluginResult = TestResult
ReporterPluginResult = Optional[None]


PluginParametersType = TypeVar(
    "PluginParametersType",
    bound=BaseModel,
    default=BaseModel,
)

PluginResultType = TypeVar(
    "PluginResultType",
    DataParserPluginResult,
    TestRunnerPluginResult,
    None.__class__,
    default=None,
)
