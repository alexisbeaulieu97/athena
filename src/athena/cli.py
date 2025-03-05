import logging
from pathlib import Path

import pluggy
import typer

from athena.models.plugin import Plugin
from athena.plugins.builtin import (
    BUILTIN_PARSER_PLUGINS,
    BUILTIN_REPORTER_PLUGINS,
    BUILTIN_TEST_RUNNER_PLUGINS,
)
from athena.plugins.hookspecs import DataParserHooks, ReporterHooks, TestRunnerHooks
from athena.protocols.data_parser_protocol import DataParserProtocol
from athena.protocols.reporter_protocol import ReporterProtocol
from athena.protocols.test_runner_protocol import TestRunnerProtocol
from athena.services.config_parser_service import ConfigParserService
from athena.services.plugin_service import PluginService
from athena.services.report_service import ReportService
from athena.services.test_service import TestService
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
        plugin_manager = pluggy.PluginManager("athena")
        plugin_manager.add_hookspecs(DataParserHooks)
        plugin_manager.add_hookspecs(TestRunnerHooks)
        plugin_manager.add_hookspecs(ReporterHooks)
        plugin_manager.load_setuptools_entrypoints("athena.plugins")

        for plugin in (
            BUILTIN_PARSER_PLUGINS
            + BUILTIN_TEST_RUNNER_PLUGINS
            + BUILTIN_REPORTER_PLUGINS
        ):
            plugin_manager.register(plugin)

        # Create plugin services for different plugin types
        data_parser_plugin_service = PluginService[Plugin[DataParserProtocol]]()
        data_parser_plugin_service.register_plugins(
            plugin_manager.hook.activate_data_parser_plugin()
        )
        test_runner_plugin_service = PluginService[Plugin[TestRunnerProtocol]]()
        test_runner_plugin_service.register_plugins(
            plugin_manager.hook.activate_test_plugin()
        )
        reporter_plugin_service = PluginService[Plugin[ReporterProtocol]]()
        reporter_plugin_service.register_plugins(
            plugin_manager.hook.activate_reporter_plugin()
        )

        # Initialize core services
        data_parser_service = ConfigParserService(data_parser_plugin_service)
        test_service = TestService(test_runner_plugin_service, data_parser_service)
        report_service = ReportService(reporter_plugin_service)

        # Create the main test suite service with the required service protocols
        test_suite_service = TestSuiteService(
            data_parser_service,
            test_service,
            report_service,
        )

        # Run the tests
        test_suite_service.run_tests_from_config(config_file)
    except Exception as e:
        logger.exception("Error running tests")
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
