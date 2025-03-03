from pathlib import Path
from athena.services.configuration_service import ConfigurationService
from athena.services.report_service import ReportService
from athena.services.test_service import TestService
from athena.plugins.data_parser_plugins_manager import DataParserPluginsManager
from athena.plugins.report_plugins_manager import ReportPluginsManager
from athena.plugins.test_plugins_manager import TestPluginsManager
from athena.models.test_suite_summary import TestSuiteSummary


class AthenaTestService:
    def __init__(self, project_name: str) -> None:
        self.parser_plugins_manager = DataParserPluginsManager(project_name)
        self.test_plugins_manager = TestPluginsManager(project_name)
        self.report_plugins_manager = ReportPluginsManager(project_name)
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
