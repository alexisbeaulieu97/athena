"""Rich Console reporter plugin for Athena test reports."""

from enum import Enum
from typing import Any

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from athena.models.plugin import Plugin
from athena.models.plugin_metadata import PluginMetadata
from athena.models.test_result import ResultType
from athena.models.test_suite_summary import TestSuiteSummary
from athena.plugins import hookimpl
from athena.protocols.reporter_protocol import ReporterProtocol


class OutputFormat(str, Enum):
    """Format options for Rich Console output."""

    TABLE = "table"  # Tabular format with columns for status, name, message
    LIST = "list"  # List format with one test per item


@hookimpl
def activate_reporter_plugin() -> Plugin[ReporterProtocol]:
    """Register the Rich Console reporter plugin."""
    return Plugin(
        metadata=PluginMetadata(
            name="rich_console",
            description="Display test results in terminal with rich formatting",
        ),
        executor=RichConsoleReporter(),
        identifiers=("rich_console",),
    )


class RichConsoleReporter:
    def __init__(self) -> None:
        self.console = Console()

    def report(self, summary: TestSuiteSummary, **kwargs: Any) -> None:
        """Display test results using Rich formatting.

        Args:
            summary: Test execution summary containing results
            **kwargs: Additional parameters passed from the reporter config
        """
        # Process format setting
        format_name = kwargs.get("format", "table")
        try:
            output_format = OutputFormat(format_name)
        except ValueError:
            print(f"Warning: Unknown format '{format_name}', using 'table' instead")
            output_format = OutputFormat.TABLE

        show_details = kwargs.get("show_details", False)

        if output_format == OutputFormat.TABLE:
            self._table_format(summary)
        else:
            self._list_format(summary, show_details)

        if kwargs.get("show_summary", True):
            self._print_summary(summary)

    def _table_format(self, summary: TestSuiteSummary) -> None:
        """Print results in a clean table format."""
        table = Table(
            show_header=True,
            show_lines=True,
            box=box.ROUNDED,
        )
        table.add_column("Status", style="bold")
        table.add_column("Test Name", no_wrap=True)
        table.add_column("Message", no_wrap=True)
        table.add_column("Runner")

        for result in summary.results:
            status_style = self._get_status_style(result.result.type)
            status = Text(result.result.type.value.upper(), style=status_style)
            message = result.result.message or ""

            table.add_row(
                status, result.config.name, message, result.config.plugin_identifier
            )

        self.console.print(table)
        self.console.print()

    def _list_format(self, summary: TestSuiteSummary, show_details: bool) -> None:
        """Print results in a clean list format."""
        for idx, result in enumerate(summary.results):
            status_style = self._get_status_style(result.result.type)
            status_text = result.result.type.value.upper()

            # Create test header
            self.console.print(
                Text(f"[{status_text}]", style=status_style),
                Text(f" {result.config.name}", style="bold"),
            )

            # Show message if available
            if result.result.message:
                self.console.print(f"  Message: {result.result.message}")

            # Show test details if enabled and available
            if show_details and result.result.details:
                detail_count = len(result.result.details)
                pass_count = sum(1 for d in result.result.details.values() if d.success)
                fail_count = detail_count - pass_count

                # Show summary of details
                self.console.print(
                    f"  Details: {pass_count} passed, {fail_count} failed"
                )

                # Show first failing detail (if any)
                for key, detail in result.result.details.items():
                    if not detail.success:
                        self.console.print(f"    First failure: {key}")
                        self.console.print(f"      Expected: {detail.expected}")
                        self.console.print(f"      Actual: {detail.actual}")
                        break

            # Show runner
            self.console.print(f"  Runner: {result.config.plugin_identifier}")

            # Add separator between tests (except after the last one)
            if idx < len(summary.results) - 1:
                self.console.print("─" * 50)

    def _print_summary(self, summary: TestSuiteSummary) -> None:
        """Print overall test summary statistics."""
        # Count results by type
        total_tests = len(summary.results)
        passed = sum(1 for r in summary.results if r.result.type == ResultType.PASSED)
        failed = sum(1 for r in summary.results if r.result.type == ResultType.FAILED)
        skipped = sum(1 for r in summary.results if r.result.type == ResultType.SKIPPED)

        # Create summary table
        table = Table(show_header=False, box=None)
        table.add_column("Stat")
        table.add_column("Value", style="bold")

        table.add_row("Total Tests:", str(total_tests))
        table.add_row("Passed:", Text(str(passed), style="green bold"))
        table.add_row("Failed:", Text(str(failed), style="red bold"))
        table.add_row("Skipped:", Text(str(skipped), style="yellow bold"))

        # Calculate success rate
        if total_tests > 0:
            success_rate = (passed / total_tests) * 100
            success_text = f"{success_rate:.1f}%"
            success_style = (
                "green bold"
                if success_rate == 100
                else "yellow bold"
                if success_rate >= 80
                else "red bold"
            )
            table.add_row("Success Rate:", Text(success_text, style=success_style))

        self.console.print(
            Panel(
                table,
                title="Summary",
                border_style="cyan",
                expand=False,
            )
        )

    def _get_status_style(self, status: ResultType) -> str:
        """Get the appropriate style for a status."""
        if status == ResultType.PASSED:
            return "green bold"
        elif status == ResultType.FAILED:
            return "red bold"
        else:  # SKIPPED
            return "yellow bold"
