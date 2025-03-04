from pathlib import Path

from athena.models.test_suite_summary import TestSuiteSummary
from athena.protocols.data_parser_plugins_manager_protocol import (
    DataParserPluginsManagerProtocol,
)
from athena.protocols.report_plugins_manager_protocol import (
    ReportPluginsManagerProtocol,
)
from athena.protocols.test_plugins_manager_protocol import TestPluginsManagerProtocol
from athena.services.configuration_service import ConfigurationService
from athena.services.report_service import ReportService
from athena.services.test_service import TestService


class TestSuiteService:
    def __init__(
        self,
        parser_plugins_manager: DataParserPluginsManagerProtocol,
        test_plugins_manager: TestPluginsManagerProtocol,
        report_plugins_manager: ReportPluginsManagerProtocol,
    ) -> None:
        self.parser_plugins_manager = parser_plugins_manager
        self.test_plugins_manager = test_plugins_manager
        self.report_plugins_manager = report_plugins_manager
        self.config_manager = ConfigurationService(self.parser_plugins_manager)

        self.initialize_plugins()

    def initialize_plugins(self) -> None:
        """Initialize all plugin managers."""
        for manager in [
            self.parser_plugins_manager,
            self.test_plugins_manager,
            self.report_plugins_manager,
        ]:
            manager.load_builtin_plugins()
            manager.load_plugins()

    def run_tests_from_config(self, config_file: Path) -> TestSuiteSummary:
        """Run all tests defined in the configuration file."""
        config = self.config_manager.parse_config(config_file)
        if not config:
            raise ValueError(f"Failed to parse configuration file: {config_file}")

        test_manager = TestService(self.test_plugins_manager, self.config_manager)
        results = test_manager.run_tests(config)

        report_manager = ReportService(self.report_plugins_manager)
        report_manager.generate_reports(config, results)

        return TestSuiteSummary(results=results)
