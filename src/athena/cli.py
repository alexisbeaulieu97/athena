from pathlib import Path
from typing import Any, Optional

import typer

from athena.models import TestConfig, TestResult
from athena.plugins.plugin_manager import pm

app = typer.Typer()


def import_config(config_raw: str, format: str) -> Optional[dict[str, Any]]:
    """Import configuration from raw string."""
    return pm.hook.parse_raw_data(data=config_raw, format=format)


def execute_test(config: TestConfig) -> TestResult:
    """Execute test based on the configuration."""
    summary = pm.hook.run_test(config=config.parameters)
    return summary


@app.command()
def run(
    config_file: Path = typer.Argument(..., help="The path to the config file"),
    config_format: str = typer.Option("yaml", help="The config format to use"),
) -> None:
    try:
        # Read configuration file for tests
        config_raw = config_file.read_text()
        config = import_config(config_raw, format=config_format)
        if config is None:
            typer.echo(
                f"Failed to import configuration using format: {config_format}",
                err=True,
            )
            raise typer.Exit(1)

        # Execute tests based on the configuration
        for test_config in config.get("tests", []):
            result = execute_test(TestConfig(**test_config))
            typer.echo(result)

        # Handle report generation using the results

    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
