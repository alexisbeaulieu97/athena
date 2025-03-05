"""JSON export plugin for Athena test reports."""

import json
from datetime import datetime

from athena.models import BaseModel
from athena.models.plugin import Plugin
from athena.models.plugin_metadata import PluginMetadata
from athena.models.test_suite_summary import TestSuiteSummary
from athena.plugins import hookimpl
from athena.types import ReporterPluginResult


class JSONReporterParameters(BaseModel):
    summary: TestSuiteSummary


@hookimpl
def activate_reporter_plugin() -> Plugin[
    ReporterPluginResult,
    JSONReporterParameters,
]:
    """Register the JSON reporter plugin."""
    return Plugin(
        metadata=PluginMetadata(
            name="json",
            description="Export test results as JSON file",
        ),
        executor=JSONReporter(),
        parameters_model=JSONReporterParameters,
        identifiers={"json"},
    )


class JSONReporter:
    def __call__(self, parameters: JSONReporterParameters) -> ReporterPluginResult:
        """Export test results as JSON file.

        Args:
            summary: Test execution summary containing results and statistics
        """
        # Generate filename with timestamp for uniqueness
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"athena_report_{timestamp}.json"

        # Convert the summary to JSON with custom encoder
        with open(filename, "w") as f:
            json.dump(parameters.summary.model_dump(), f, indent=2)

        print(f"Report exported to: {filename}")
