from typing import Any, Optional

import yaml

from athena.plugins import hookimpl


@hookimpl
def parse_raw_data(
    data: Any,
    format: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    """Parse raw YAML data."""
    if format not in ["yaml", "yml"]:
        return None
    return yaml.safe_load(data)
