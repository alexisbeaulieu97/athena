from heapq import merge
import logging
from pathlib import Path
from typing import Any, Optional

import typer

from athena.models.athena_test_suite_config import AthenaTestSuiteConfig
from athena.plugins.plugin_manager import pm
from athena.models.test_config import TestConfig
from athena.models.test_suite_summary import TestSuiteSummary

app = typer.Typer()
logging.basicConfig(level=logging.DEBUG)


@app.command()
def run(
    config_file: Path = typer.Argument(..., help="The path to the config file"),
) -> None:
    try:
        # Read configuration file for tests
        config_raw = config_file.read_text()
        config_obj = pm.parse_data(config_raw, format=config_file.suffix.lstrip("."))
        if not config_obj:
            typer.echo(
                f"Failed to parse configuration using format: {config_file.suffix.lstrip('.')}",
                err=True,
            )
            raise typer.Exit(1)
        config = AthenaTestSuiteConfig(**config_obj)

        # Execute tests based on the configuration
        results = []
        for test_config in config.tests:
            # Merge global parameters with test-specific ones
            merged_params = {}
            if config.parameters:
                merged_params = config.parameters.copy()
            if test_config.parameters:
                merged_params.update(test_config.parameters)
            test_config.parameters = merged_params

            result = pm.run_test(test_config)
            results.append(result)
            typer.echo(result)

        # Create a test suite summary with the results
        summary = TestSuiteSummary(results=results)
        for report in config.reports:
            pm.report(report, summary)

    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
