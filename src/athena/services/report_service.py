from athena.models import BaseModel
from athena.models.test_suite_config import TestSuiteConfig
from athena.models.test_suite_summary import TestSuiteSummary
from athena.protocols.plugin_service_protocol import PluginServiceProtocol
from athena.types import ReporterPluginResult


class ReportService:
    """Component responsible for generating reports."""

    def __init__(
        self,
        plugin_service: PluginServiceProtocol[ReporterPluginResult, BaseModel],
    ) -> None:
        self.plugin_service = plugin_service

    def generate_reports(
        self, config: TestSuiteConfig, summary: TestSuiteSummary
    ) -> None:
        """Generate reports using the configured reporters."""
        for report in config.reports:
            plugin = self.plugin_service.get_plugin(report.plugin_identifier)
            plugin.executor(
                plugin.parameters_model(
                    **{
                        "summary": summary,
                        **config.model_dump(),
                    },
                )
            )
