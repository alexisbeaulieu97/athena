from typing import Any, Dict, Optional

from athena.models import TestResult, TestSummary
from athena.plugins import hookspec


@hookspec
def athena_import_config(config: str, format: Optional[str] = None) -> Optional[dict[str, Any]]:
    """Hook specification for importing configuration.

    Args:
        config: The configuration string to parse
        format: Optional format specifier ('json', 'yaml', etc.)

    Returns:
        Parsed configuration as dict if format matches, None otherwise
    """
    pass

@hookspec
def athena_run_test(name: str, config: Dict[str, Any]) -> TestResult:
    """Run a test with the given configuration.

    Args:
        name: Test name
        config: Test configuration

    Returns:
        TestResult: Test execution result
    """
    pass

@hookspec
def athena_export_config(config: dict[str, Any], format: Optional[str] = None) -> Optional[str]:
    """Hook specification for exporting configuration.

    Args:
        config: The configuration dictionary to format
        format: Optional format specifier ('json', 'yaml', etc.)

    Returns:
        Formatted configuration as string if format matches, None otherwise
    """
    pass

@hookspec
def athena_register_test() -> Dict[str, Any]:
    """Register a test plugin.

    Returns:
        Dict with keys:
            name: Test plugin name
            version: Test plugin version
            description: Test plugin description
            dependencies: List of plugin dependencies
    """
    pass

@hookspec
def athena_handle_report(summary: TestSummary) -> None:
    """Handle test execution report.

    Args:
        summary: Test execution summary containing results and statistics

    This hook can be used to:
    - Print to stdout
    - Save to file
    - Send to external API
    - Generate HTML report
    - etc.
    """
    pass
