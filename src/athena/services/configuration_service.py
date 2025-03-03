from pathlib import Path
from typing import Optional

from athena.models.athena_test_suite_config import AthenaTestSuiteConfig
from athena.protocols.data_parser_plugins_manager_protocol import (
    DataParserPluginsManagerProtocol,
)


class ConfigurationService:
    """Component responsible for configuration parsing and parameter management."""

    def __init__(self, plugin_manager: DataParserPluginsManagerProtocol) -> None:
        self.plugin_manager = plugin_manager

    def parse_config(self, config_file: Path) -> Optional[AthenaTestSuiteConfig]:
        """Parse a configuration file using the appropriate plugin."""
        config_raw = config_file.read_text()
        format_ext = config_file.suffix.lstrip(".")
        config_obj = self.plugin_manager.parse_data(config_raw, format=format_ext)

        if not config_obj:
            return None

        return AthenaTestSuiteConfig(**config_obj)

    def merge_parameters(self, global_params: dict, test_params: dict) -> dict:
        """Merge global and test-specific parameters with proper precedence."""
        if not global_params and not test_params:
            return {}

        merged_params = {}
        if global_params:
            merged_params = global_params.copy()
        if test_params:
            merged_params.update(test_params)

        return merged_params
