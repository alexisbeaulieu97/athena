# from athena.models.data_parser_plugin import DataParserPlugin
from athena.models.plugin import Plugin

# from athena.models.reporter_plugin import ReporterPlugin
# from athena.models.test_plugin import TestPlugin
from athena.plugins import hookspec
from athena.protocols.data_parser_protocol import DataParserProtocol
from athena.protocols.reporter_protocol import ReporterProtocol
from athena.protocols.test_runner_protocol import TestRunnerProtocol


class DataParserHooks:
    @hookspec
    def activate_data_parser_plugin() -> Plugin[DataParserProtocol]:
        """Register a raw data parser."""
        ...


class TestRunnerHooks:
    @hookspec
    def activate_test_plugin() -> Plugin[TestRunnerProtocol]:
        """Register a test runner."""
        ...


class ReporterHooks:
    @hookspec
    def activate_reporter_plugin() -> Plugin[ReporterProtocol]:
        """Register a test result reporter."""
        ...
