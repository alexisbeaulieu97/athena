from pathlib import Path

from athena.models import BaseModel
from athena.models.test_suite_config import TestSuiteConfig
from athena.models.test_suite_summary import TestSuiteSummary
from athena.protocols.config_parser_service_protocol import ConfigParserServiceProtocol
from athena.protocols.plugin_service_protocol import PluginServiceProtocol
from athena.protocols.report_service_protocol import ReportServiceProtocol
from athena.protocols.test_service_protocol import TestServiceProtocol
from athena.types import DataParserPluginResult


class TestSuiteService:
    def __init__(
        self,
        data_parser_service: ConfigParserServiceProtocol,
        test_service: TestServiceProtocol,
        report_service: ReportServiceProtocol,
        plugin_service: PluginServiceProtocol[DataParserPluginResult, BaseModel],
    ) -> None:
        self.data_parser_service = data_parser_service
        self.test_service = test_service
        self.report_service = report_service
        self.plugin_service = plugin_service

    def run_tests_from_config(self, config_file: Path) -> None:
        """Run all tests defined in the configuration file."""
        config = self.data_parser_service.parse(config_file, self.plugin_service)
        if not config:
            raise ValueError("Configuration file is empty")
        test_suite_config = TestSuiteConfig(**config)
        results = self.test_service.run_tests(test_suite_config)

        self.report_service.generate_reports(
            test_suite_config,
            TestSuiteSummary(results=results),
        )
