import logging
from pathlib import Path
from typing import Any, Dict, Optional

import typer

from athena.models import TestConfig, TestResult, TestRunnerProtocol, TestSuiteSummary
from athena.plugins.builtin import BUILTIN_PLUGINS
from athena.plugins.builtin.custom_runner import get_runners
from athena.plugins.plugin_manager import pm as legacy_pm
from athena.service import ConfigService, PluginService, TestService

# Create a Typer app for the CLI
app = typer.Typer()

# Set up services
plugin_service = PluginService()
config_service = ConfigService(plugin_service)
test_service = TestService(plugin_service)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DirectRunnerProvider:
    """Provider for directly registering test runners."""

    def __init__(self, runners: Dict[str, TestRunnerProtocol]):
        """Initialize with a dictionary of runners.

        Args:
            runners: Dictionary mapping runner names to TestRunnerProtocol instances
        """
        self.runners = runners

    def get_parsers(self):
        """Get parsers (none for this provider)."""
        return []

    def get_runners(self):
        """Get the dictionary of runners."""
        return self.runners

    def get_reporters(self):
        """Get reporters (none for this provider)."""
        return []


def setup_plugins() -> None:
    """Set up plugins from various sources."""
    # Register built-in plugins
    for plugin in BUILTIN_PLUGINS:
        plugin_service.register_plugin(plugin)

    # Register custom runners
    custom_runners = get_runners()
    plugin_service.register_provider(DirectRunnerProvider(custom_runners))

    # For backwards compatibility, also register plugins from the legacy manager
    for name, test_plugin in legacy_pm.tests.items():

        class LegacyPlugin:
            def register_test(self):
                return [test_plugin]

        plugin_service.register_plugin(LegacyPlugin())


@app.command()
def run(
    config_file: Path = typer.Argument(..., help="The path to the config file"),
    config_format: str = typer.Option("yaml", help="The config format to use"),
) -> None:
    """Run tests from a configuration file."""
    try:
        # Ensure plugins are set up
        setup_plugins()

        # Read and parse configuration file
        config_raw = config_file.read_text()
        config_dict = config_service.parse_config(config_raw, format=config_format)

        if config_dict is None:
            typer.echo(
                f"Failed to parse configuration using format: {config_format}",
                err=True,
            )
            raise typer.Exit(1)

        # Build test suite config
        suite_config = config_service.build_test_suite(config_dict)

        # Run the test suite
        summary = test_service.run_test_suite(suite_config)

        # Display results
        for result in summary.results:
            typer.echo(result)

    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)


@app.command()
def list_runners():
    """List available test runners."""
    # Ensure plugins are set up
    setup_plugins()

    typer.echo("Available test runners:")
    for name in plugin_service.runners.keys():
        typer.echo(f"  - {name}")


def main() -> None:
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
