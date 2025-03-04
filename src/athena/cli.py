import logging
from pathlib import Path

import typer

from athena.plugins.data_parser_plugins_manager import DataParserPluginsManager
from athena.plugins.report_plugins_manager import ReportPluginsManager
from athena.plugins.test_plugins_manager import TestPluginsManager
from athena.services.test_suite_service import TestSuiteService

app = typer.Typer()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.command()
def run(
    config_file: Path = typer.Argument(..., help="The path to the config file"),
    verbose: bool = typer.Option(
        False, "-v", "--verbose", help="Enable verbose logging"
    ),
) -> None:
    """Run tests based on the provided configuration file."""

    # Set logging level based on verbosity
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        data_parser_plugins_manager = DataParserPluginsManager("athena")
        test_plugins_manager = TestPluginsManager("athena")
        report_plugins_manager = ReportPluginsManager("athena")
        test_service = TestSuiteService(
            data_parser_plugins_manager,
            test_plugins_manager,
            report_plugins_manager,
        )
        summary = test_service.run_tests_from_config(config_file)

        # Show summary
        passed = sum(1 for r in summary.results if r.status == "passed")
        failed = sum(1 for r in summary.results if r.status == "failed")
        skipped = sum(1 for r in summary.results if r.status == "skipped")

        typer.echo("\nTest Summary:")
        typer.echo(f"  Total: {len(summary.results)}")
        typer.secho(
            f"  Passed: {passed}", fg=typer.colors.GREEN if passed > 0 else None
        )
        typer.secho(f"  Failed: {failed}", fg=typer.colors.RED if failed > 0 else None)
        typer.secho(
            f"  Skipped: {skipped}", fg=typer.colors.YELLOW if skipped > 0 else None
        )
    except Exception as e:
        logger.exception("Error running tests")
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
