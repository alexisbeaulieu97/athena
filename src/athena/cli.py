import logging
from pathlib import Path
from typing import Optional

import typer

from athena.managers.configuration_manager import ConfigurationManager
from athena.managers.report_manager import ReportManager
from athena.managers.test_manager import TestManager
from athena.plugins.plugin_manager import AthenaPluginManager
from athena.protocols.plugin_manager_protocol import PluginManagerProtocol

app = typer.Typer()
logging.basicConfig(level=logging.DEBUG)


class Athena:
    """Main application class that orchestrates the test execution process."""

    def __init__(
        self,
        plugin_manager: PluginManagerProtocol,
        config_manager: Optional[ConfigurationManager] = None,
        test_executor: Optional[TestManager] = None,
        report_manager: Optional[ReportManager] = None,
    ) -> None:
        """Initialize with component managers for clear separation of responsibilities."""
        self.plugin_manager = plugin_manager
        self.config_manager = config_manager or ConfigurationManager(plugin_manager)
        self.test_executor = test_executor or TestManager(
            plugin_manager, self.config_manager
        )
        self.report_manager = report_manager or ReportManager(plugin_manager)

    def run_test_suite(self, config_file: Path) -> None:
        """Execute the entire test suite process."""
        # Parse configuration
        config = self.config_manager.parse_config(config_file)
        if not config:
            typer.echo(
                f"Failed to parse configuration using format: {config_file.suffix.lstrip(".")}",
                err=True,
            )
            raise typer.Exit(1)

        # Run tests
        results = self.test_executor.run_tests(config)

        # Generate reports
        self.report_manager.generate_reports(config, results)


# Create a module-level factory function for dependency injection
def create_plugin_manager(
    entrypoint_name: str = "athena.plugins",
) -> PluginManagerProtocol:
    """Factory function to create a plugin manager instance."""
    return AthenaPluginManager(entrypoint_name=entrypoint_name)


# Create a module-level factory function for creating Athena instances
def create_athena(
    plugin_manager: Optional[PluginManagerProtocol] = None,
    config_manager: Optional[ConfigurationManager] = None,
    test_executor: Optional[TestManager] = None,
    report_manager: Optional[ReportManager] = None,
) -> Athena:
    """Factory function to create an Athena instance with its dependencies."""
    plugin_manager = plugin_manager or create_plugin_manager()
    return Athena(
        plugin_manager=plugin_manager,
        config_manager=config_manager,
        test_executor=test_executor,
        report_manager=report_manager,
    )


@app.command()
def run(
    config_file: Path = typer.Argument(..., help="The path to the config file"),
) -> None:
    """Run tests based on the provided configuration file."""
    try:
        # Use the factory method instead of direct instantiation
        athena = create_athena()
        athena.run_test_suite(config_file)
    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
