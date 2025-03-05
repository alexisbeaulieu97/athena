from athena.models.plugin import Plugin
from athena.plugins import hookspec
from athena.types import (
    DataParserPluginResult,
    ReporterPluginResult,
    TestRunnerPluginResult,
)


class DataParserHooks:
    @hookspec
    def activate_data_parser_plugin() -> Plugin[DataParserPluginResult]:
        """Register a raw data parser."""
        ...


class TestRunnerHooks:
    @hookspec
    def activate_test_plugin() -> Plugin[TestRunnerPluginResult]:
        """Register a test runner."""
        ...


class ReporterHooks:
    @hookspec
    def activate_reporter_plugin() -> Plugin[ReporterPluginResult]:
        """Register a test result reporter."""
        ...
