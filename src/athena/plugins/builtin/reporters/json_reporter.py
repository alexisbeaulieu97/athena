"""JSON export plugin for Athena test reports."""

import json
from datetime import datetime
from typing import Any

from athena.models.plugin import Plugin
from athena.models.plugin_metadata import PluginMetadata
from athena.models.test_suite_summary import TestSuiteSummary
from athena.plugins import hookimpl
from athena.protocols.reporter_protocol import ReporterProtocol


@hookimpl
def activate_reporter_plugin() -> Plugin[ReporterProtocol]:
    """Register the JSON reporter plugin."""
    return Plugin(
        metadata=PluginMetadata(
            name="json",
            description="Export test results as JSON file",
        ),
        executor=JSONReporter(),
        identifiers=("json",),
    )


class JSONReporter:
    def report(self, summary: TestSuiteSummary, **kwargs: Any) -> None:
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
