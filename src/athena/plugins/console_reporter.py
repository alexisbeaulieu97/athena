import typer

from athena.models import TestStatus, TestSuiteSummary
from athena.plugins import hookimpl


class ConsoleReporter:
    @hookimpl
    def athena_handle_report(self, summary: TestSuiteSummary) -> None:
        typer.echo("\nTest Summary:")
        typer.echo(f"Timestamp: {summary.timestamp}")
        typer.echo(f"Total execution time: {summary.execution_time:.3f}s")

        for status, count in summary.summary.items():
            color = {
                "success": typer.colors.GREEN,
                "failed": typer.colors.RED,
                "skipped": typer.colors.YELLOW,
                "error": typer.colors.RED,
            }[status]
            typer.echo(f"{status.capitalize()}: ", nl=False)
            typer.secho(f"{count}", fg=color)
        typer.echo("")

        for result in summary.results:
            color = {
                TestStatus.SUCCESS: typer.colors.GREEN,
                TestStatus.FAILED: typer.colors.RED,
                TestStatus.SKIPPED: typer.colors.YELLOW,
                TestStatus.ERROR: typer.colors.RED,
            }[result.status]

            typer.echo(f"[{result.plugin_name} v{result.test_version}] {result.test_name}: ", nl=False)
            typer.secho(f"{result.status}", fg=color)
            typer.echo(f"  Duration: {result.duration:.3f}s")
            if result.message:
                typer.echo(f"  {result.message}")
            if result.details:
                typer.echo("  Details:")
                for k, v in result.details.items():
                    typer.echo(f"    {k}: {v}")
            typer.echo("")
