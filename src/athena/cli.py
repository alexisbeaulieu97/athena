from pathlib import Path
from typing import Any, Dict, Optional
import typer

from athena.models import TestConfig, TestResult, TestSuiteConfig, TestSuiteSummary
from athena.plugins.plugin_manager import pm
from athena.strategies import STRATEGIES

app = typer.Typer()


def import_config(config_raw: str, format: str) -> Optional[dict[str, Any]]:
    """Import configuration from raw string."""
    return pm.hook.parse_raw_data(data=config_raw, format=format)


@app.command()
def run(
    config_file: Path = typer.Argument(..., help="The path to the config file"),
    config_format: str = typer.Option("yaml", help="The config format to use"),
    strategy: Optional[str] = typer.Option(
        None, "--strategy", "-s", help="Test execution strategy (sequential, parallel)"
    ),
    workers: Optional[int] = typer.Option(
        None, "--workers", "-w", help="Number of workers for parallel execution"
    ),
) -> None:
    """Run tests from a configuration file using the specified execution strategy."""
    try:
        # Read configuration file for tests
        config_raw = config_file.read_text()
        config_dict = import_config(config_raw, format=config_format)
        if config_dict is None:
            typer.echo(
                f"Failed to import configuration using format: {config_format}",
                err=True,
            )
            raise typer.Exit(1)

        # Extract tests from configuration
        test_configs = []
        for test_dict in config_dict.get("tests", []):
            test_configs.append(TestConfig(**test_dict))

        # Create a test suite configuration
        suite_config = TestSuiteConfig(
            tests=test_configs,
            parameters=config_dict.get("parameters", {}),
            execution_strategy=config_dict.get("execution_strategy"),
        )

        # Override execution strategy if specified on command line
        strategy_name = strategy or suite_config.execution_strategy

        # Prepare strategy options
        strategy_options: Dict[str, Any] = {}
        if workers is not None and strategy_name == "parallel":
            strategy_options["max_workers"] = workers

        # Log execution strategy
        if strategy_name:
            typer.echo(f"Using execution strategy: {strategy_name}")

        # Run the test suite
        results = pm.run_test_suite(
            suite_config, strategy_name=strategy_name, strategy_options=strategy_options
        )

        # Display individual test results
        for result in results:
            typer.echo(result)

        # Create a test suite summary
        summary = TestSuiteSummary(results=results)

        # Let plugins handle the report
        pm.hook.handle_report(summary=summary)

    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)


@app.command()
def list_strategies() -> None:
    """List available test execution strategies."""
    typer.echo("Available test execution strategies:")
    for name, strategy_class in STRATEGIES.items():
        typer.echo(f"  - {name}: {strategy_class.__doc__}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
