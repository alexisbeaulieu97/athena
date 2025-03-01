import json
from typing import Any, Optional

from athena.plugins import hookimpl


@hookimpl
def parse_raw_data(
    data: Any,
    format: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    """Parse raw JSON data."""
    if format != "json":
        return None
    return json.loads(data)
