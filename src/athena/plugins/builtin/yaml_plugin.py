from typing import Any, Optional

import yaml

from athena.plugins import hookimpl


@hookimpl
def parse_raw_data(data: Any, format: Optional[str] = None) -> Optional[dict[str, Any]]:
    """Parse YAML formatted data."""
    if format and format.lower() not in ("yaml", "yml"):
        return None

    try:
        return yaml.safe_load(data)
    except yaml.YAMLError:
        return None
