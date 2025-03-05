from pathlib import Path
from typing import Any, Dict

from athena.models.test_suite_config import TestSuiteConfig
from athena.models.test_suite_summary import TestSuiteSummary
from athena.protocols.data_parser_service_protocol import DataParserServiceProtocol
from athena.protocols.report_service_protocol import ReportServiceProtocol
from athena.protocols.test_service_protocol import TestServiceProtocol


class TestSuiteService:
    def __init__(
        self,
        data_parser_service: DataParserServiceProtocol[Path, Dict[str, Any]],
        test_service: TestServiceProtocol,
        report_service: ReportServiceProtocol,
    ) -> None:
        self.data_parser_service = data_parser_service
        self.test_service = test_service
        self.report_service = report_service

    def run_tests_from_config(self, config_file: Path) -> None:
        """Run all tests defined in the configuration file."""
        config = self.data_parser_service.parse_data(config_file)
        if not config:
            raise ValueError("Configuration file is empty")
        test_suite_config = TestSuiteConfig(**config)
        results = self.test_service.run_tests(test_suite_config)

        self.report_service.generate_reports(
            test_suite_config,
            TestSuiteSummary(results=results),
        )
