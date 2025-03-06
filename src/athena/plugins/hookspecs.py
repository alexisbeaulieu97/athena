from athena.models import BaseModel
from athena.models.plugin import Plugin
from athena.plugins import hookspec
from athena.types import (
    DataParserPluginResult,
    ReporterPluginResult,
    TestRunnerPluginResult,
)


class DataParserHooks:
    @hookspec
    def activate_data_parser_plugin() -> Plugin[DataParserPluginResult, BaseModel]:
        """Register a raw data parser."""
        ...


class TestRunnerHooks:
    @hookspec
    def activate_test_plugin() -> Plugin[TestRunnerPluginResult, BaseModel]:
        """Register a test runner."""
        ...


class ReporterHooks:
    @hookspec
    def activate_reporter_plugin() -> Plugin[ReporterPluginResult, BaseModel]:
        """Register a test result reporter."""
        ...
