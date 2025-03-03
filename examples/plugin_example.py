"""Example of a third-party plugin for Athena.

This file demonstrates how to create a plugin that can be installed
via pip and registered using setuptools entrypoints.

To use this plugin, you would include it in your package and add an
entry_points section to your setup.py or pyproject.toml:

```python
# setup.py
setup(
    name="my-athena-plugin",
    # ...
    entry_points={
        "athena.plugins": [
            "my-plugin=my_package.plugin_module:create_plugin",
        ],
    },
)
```

```toml
# pyproject.toml
[project.entry-points."athena.plugins"]
my-plugin = "my_package.plugin_module:create_plugin"
```
"""

import platform
import socket
from typing import Dict, List, Optional

from athena.models import (
    ConfigParserProtocol,
    PluginMetadata,
    ReporterProtocol,
    TestConfig,
    TestDetails,
    TestFailedResult,
    TestPassedResult,
    TestResult,
    TestRunnerProtocol,
    TestSkippedResult,
    TestSuiteSummary,
)


class NetworkTestRunner(TestRunnerProtocol):
    """Test runner for network connectivity tests."""

    def __init__(self):
        """Initialize the network test runner."""
        self.metadata = PluginMetadata(
            name="network",
            version="1.0.0",
            description="Tests network connectivity to specified hosts",
        )

    def run(self, config: TestConfig) -> TestResult:
        """Run network connectivity tests.

        Args:
            config: Test configuration

        Returns:
            Test result
        """
        # Extract parameters
        hosts = config.parameters.get("hosts", [])
        timeout = config.parameters.get("timeout", 1)  # 1 second timeout by default

        # Skip if no hosts configured
        if not hosts:
            return TestSkippedResult(message="No hosts configured for network test")

        # Test connectivity to each host
        details = {}
        all_successful = True

        for host in hosts:
            try:
                # Try to establish a connection
                with socket.create_connection((host, 80), timeout=timeout) as _:
                    details[host] = TestDetails(
                        expected="Connection established",
                        actual="Connection successful",
                        success=True,
                    )
            except Exception as e:
                details[host] = TestDetails(
                    expected="Connection established",
                    actual=f"Connection failed: {str(e)}",
                    success=False,
                )
                all_successful = False

        # Return appropriate result
        if all_successful:
            return TestPassedResult(
                message="All network connections successful",
                details=details,
            )
        else:
            return TestFailedResult(
                message="Some network connections failed",
                details=details,
            )


class CsvReporter(ReporterProtocol):
    """Reporter that exports test results to a CSV file."""

    def report(self, summary: TestSuiteSummary) -> None:
        """Generate a CSV report from test results.

        Args:
            summary: The test suite summary containing results
        """
        import csv
        from datetime import datetime

        # Create a CSV file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"athena_report_{timestamp}.csv"

        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)

            # Write header row
            writer.writerow(["Result Type", "Message", "Details"])

            # Write data rows
            for result in summary.results:
                result_type = result.__class__.__name__
                message = result.message or ""

                # Process details if available
                details_str = ""
                if hasattr(result, "details") and result.details:
                    details_parts = []
                    for key, detail in result.details.items():
                        details_parts.append(
                            f"{key}: expected={detail.expected}, actual={detail.actual}, success={detail.success}"
                        )
                    details_str = "; ".join(details_parts)

                writer.writerow([result_type, message, details_str])

        print(f"CSV report written to {filename}")


class MyPluginProvider:
    """Provider for all components in this plugin."""

    def __init__(self):
        """Initialize the plugin provider."""
        self.network_runner = NetworkTestRunner()
        self.csv_reporter = CsvReporter()

    def get_parsers(self) -> List[ConfigParserProtocol]:
        """Get configuration parsers (none for this plugin)."""
        return []

    def get_runners(self) -> Dict[str, TestRunnerProtocol]:
        """Get test runners provided by this plugin."""
        return {"network": self.network_runner}

    def get_reporters(self) -> List[ReporterProtocol]:
        """Get reporters provided by this plugin."""
        return [self.csv_reporter]


# Factory function that will be called when the plugin is loaded via entrypoint
def create_plugin():
    """Create and return the plugin provider.

    This function is the entrypoint that Athena will call to load the plugin.

    Returns:
        A plugin provider instance
    """
    return MyPluginProvider()


# If this module is imported directly (not via entrypoint),
# this allows manual registration of the plugin
plugin_provider = create_plugin()