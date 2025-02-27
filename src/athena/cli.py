from pathlib import Path

import typer

from athena.plugins.plugin_manager import PluginManager

app = typer.Typer()


@app.command()
def run(
    config_file: Path = typer.Argument(..., help="The path to the config file"),
    config_format: str = typer.Option("yaml", help="The config format to use"),
    report_format: str = typer.Option("console", help="The report format to use"),
):
    pm = PluginManager()
    try:
        config_raw = config_file.read_text()
        config = pm.import_config(config_raw, format=config_format)
        if config is None:
            typer.echo(f"Failed to import configuration using format: {config_format}", err=True)
            raise typer.Exit(1)

        # Run tests
        summary = pm.run_test(config)

        # Handle report with specified format
        pm.handle_report(summary)

    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)

def main():
    app()


if __name__ == "__main__":
    main()
