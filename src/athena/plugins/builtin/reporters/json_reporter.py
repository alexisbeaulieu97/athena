"""JSON export plugin for Athena test reports."""

import json
from datetime import datetime

from athena.models.plugin_metadata import PluginMetadata
from athena.models.reporter_plugin import ReporterPlugin
from athena.models.test_suite_summary import TestSuiteSummary
from athena.plugins import hookimpl


@hookimpl(tryfirst=True)
def register_reporter_plugin() -> ReporterPlugin:
    """Register the JSON reporter plugin."""
    return ReporterPlugin(
        metadata=PluginMetadata(
            name="json",
            description="Export test results as JSON file",
        ),
        reporter=JSONReporter(),
    )


class JSONReporter:
    def report(self, summary: TestSuiteSummary) -> None:
        """Export test results as JSON file.

        Args:
            summary: Test execution summary containing results and statistics
        """
        # Generate filename with timestamp for uniqueness
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"athena_report_{timestamp}.json"

        # Convert the summary to JSON with custom encoder
        with open(filename, "w") as f:
            json.dump(summary.model_dump(), f, indent=2)

        print(f"Report exported to: {filename}")
