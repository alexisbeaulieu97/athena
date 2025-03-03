from heapq import merge
import logging
from pathlib import Path
from typing import Any, Optional

import typer
from typing_extensions import Annotated

from athena.models.athena_test_suite_config import AthenaTestSuiteConfig
from athena.plugins.plugin_manager import AthenaPluginManager
from athena.models.test_config import TestConfig
from athena.models.test_suite_summary import TestSuiteSummary

app = typer.Typer()
logging.basicConfig(level=logging.DEBUG)


class Athena:
    """Main application class that handles test execution."""

    def __init__(self, plugin_manager: AthenaPluginManager) -> None:
        """Initialize with an optional plugin manager for dependency injection."""
        self.plugin_manager = plugin_manager or default_plugin_manager

    def parse_config(self, config_file: Path) -> Optional[AthenaTestSuiteConfig]:
        """Parse a configuration file using the appropriate plugin."""
        config_raw = config_file.read_text()
        format_ext = config_file.suffix.lstrip(".")
        config_obj = self.plugin_manager.parse_data(config_raw, format=format_ext)

        if not config_obj:
            typer.echo(
                f"Failed to parse configuration using format: {format_ext}",
                err=True,
            )
            return None

        return AthenaTestSuiteConfig(**config_obj)

    def merge_parameters(self, global_params: dict, test_params: dict) -> dict:
        """Merge global and test-specific parameters with proper precedence."""
        if not global_params and not test_params:
            return {}

        merged_params = {}
        if global_params:
            merged_params = global_params.copy()
        if test_params:
            merged_params.update(test_params)

        return merged_params

    def run_tests(self, config: AthenaTestSuiteConfig) -> list:
        """Execute tests based on the configuration."""
        results = []

        for test_config in config.tests:
            # Merge global parameters with test-specific ones
            merged_params = self.merge_parameters(
                config.parameters or {}, test_config.parameters or {}
            )

            # Create a new test config to avoid modifying the original
            test_config_copy = TestConfig(
                name=test_config.name, parameters=merged_params
            )

            result = self.plugin_manager.run_test(test_config_copy)
            results.append(result)
            typer.echo(result)

        return results

    def generate_reports(self, config: AthenaTestSuiteConfig, results: list) -> None:
        """Generate reports using the configured reporters."""
        summary = TestSuiteSummary(results=results)
        for report in config.reports:
            self.plugin_manager.report(report, summary)


@app.command()
def run(
    config_file: Path = typer.Argument(..., help="The path to the config file"),
) -> None:
    """Run tests based on the provided configuration file."""
    try:
        athena = Athena(AthenaPluginManager(entrypoint_name="athena.plugins"))

        # Parse configuration
        config = athena.parse_config(config_file)
        if not config:
            raise typer.Exit(1)

        # Run tests
        results = athena.run_tests(config)

        # Generate reports
        athena.generate_reports(config, results)

    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
