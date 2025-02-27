import json
from typing import Any, Optional

from athena.plugins.base import ConfigHandler


class JsonConfigHandler(ConfigHandler):
    format = "json"

    def _import_config(self, config: str) -> Optional[dict[str, Any]]:
        try:
            return json.loads(config)
        except json.JSONDecodeError:
            return None

    def _export_config(self, config: dict[str, Any]) -> Optional[str]:
        try:
            return json.dumps(config, indent=4)
        except TypeError:
            return None
