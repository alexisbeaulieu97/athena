from athena.models.data_parser_plugin import DataParserPlugin
from athena.models.reporter_plugin import ReporterPlugin
from athena.models.test_plugin import TestPlugin
from athena.plugins import hookspec


class DataParserHooks:
    @hookspec
    def register_data_parser_plugin() -> DataParserPlugin:
        """Register a raw data parser."""
        ...


class TestRunnerHooks:
    @hookspec
    def register_test_plugin() -> TestPlugin:
        """Register a test runner."""
        ...


class ReporterHooks:
    @hookspec
    def register_reporter_plugin() -> ReporterPlugin:
        """Register a test result reporter."""
        ...
