from typing import Any, Optional

import yaml

from athena.plugins.base import ConfigHandler


class YamlConfigHandler(ConfigHandler):
    format = "yaml"

    def _import_config(self, config: str) -> Optional[dict[str, Any]]:
        try:
            return yaml.safe_load(config)
        except yaml.YAMLError:
            return None

    def _export_config(self, config: dict[str, Any]) -> Optional[str]:
        try:
            return yaml.safe_dump(config, default_flow_style=False)
        except yaml.YAMLError:
            return None
