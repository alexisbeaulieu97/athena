from typing import Any, Optional

from athena.models import TestConfig, TestPlugin, TestResult, TestSuiteSummary
from athena.plugins import hookspec


@hookspec(firstresult=True)
def parse_raw_data(
    data: Any,
    format: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    """Parse raw data.

    Args:
        data: Raw data to parse
        format: Optional format specifier ('json', 'yaml', etc.)

    Returns:
        Parsed data as dict if format matches, None otherwise
    """
    ...


@hookspec
def register_test() -> TestPlugin:
    """Register a test plugin."""
    ...


@hookspec
def handle_report(summary: TestSuiteSummary) -> None:
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
    ...
