from pathlib import Path
from typing import Any, Optional

import typer

from athena.models import TestConfig, TestResult, TestSuiteSummary
from athena.plugins.plugin_manager import pm

app = typer.Typer()


def import_config(config_raw: str, format: str) -> Optional[dict[str, Any]]:
    """Import configuration from raw string."""
    return pm.hook.parse_raw_data(data=config_raw, format=format)


# In cli.py, update the run function to create a summary and call the report hook
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

        # Get global parameters
        global_params = config.get("parameters", {})

        # Execute tests based on the configuration
        results = []
        for test_config in config.get("tests", []):
            # Merge global parameters with test-specific ones
            merged_params = global_params.copy()
            merged_params.update(test_config.get("parameters", {}))
            test_config["parameters"] = merged_params

            result = pm.run_test(TestConfig(**test_config))
            results.append(result)
            typer.echo(result)

        # Create a test suite summary with the results
        summary = TestSuiteSummary(results=results)

        # Let plugins handle the report
        pm.hook.handle_report(summary=summary)

    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
