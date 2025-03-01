from pathlib import Path
from typing import Any, Optional

import typer

from athena.plugins.plugin_manager import pm

app = typer.Typer()


# def _parse_test_configs(self, config: dict[str, Any]) -> TestSuiteConfig:
#         """Parse the raw config dict into a structured TestsConfig object."""
#         if "tests" not in config:
#             return TestSuiteConfig()

#         tests_list = []
#         for test_config in config.get("tests", []):
#             if isinstance(test_config, dict):
#                 test_name = test_config.get("name")
#                 if test_name:
#                     parameters = test_config.get("parameters", {})
#                     tests_list.append(TestConfig(name=test_name, parameters=parameters))

#         global_params = {k: v for k, v in config.items() if k != "tests"}
#         return TestSuiteConfig(tests=tests_list, parameters=global_params)

#     def run_test(self, config: dict[str, Any]) -> TestSuiteSummary:
#         results = []
#         start_time = time.time()

#         # Parse config into structured format
#         tests_config = self._parse_test_configs(config)

#         # Get all registered test plugins
#         test_plugins = [p for p in self.pm.get_plugins() if hasattr(p, 'athena_register_test')]

#         # Run each configured test
#         for test_config in tests_config.tests:
#             # Merge global parameters with test-specific parameters
#             # Test-specific parameters take precedence
#             test_params = {**tests_config.parameters, **test_config.parameters}

#             # Run the test across all plugins
#             for plugin in test_plugins:
#                 result = self.pm.hook.athena_run_test(name=test_config.name, config=test_params)
#                 if result:
#                     results.extend(result)

#         return TestSuiteSummary(
#             results=results,
#             execution_time=time.time() - start_time
#         )


def import_config(config_raw: str, format: str) -> Optional[dict[str, Any]]:
    """Import configuration from raw string."""
    return pm.hook.parse_raw_data(data=config_raw, format=format)


@app.command()
def run(
    config_file: Path = typer.Argument(..., help="The path to the config file"),
    config_format: str = typer.Option("y aml", help="The config format to use"),
) -> None:
    try:
        config_raw = config_file.read_text()
        config = import_config(config_raw, format=config_format)
        if config is None:
            typer.echo(
                f"Failed to import configuration using format: {config_format}",
                err=True,
            )
            raise typer.Exit(1)

        print(config)
        # Run tests
        # summary = pm.run_test(config)

        # Handle report with specified format
        # pm.handle_report(summary)

    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
