import logging
from typing import Any, Dict, List, Optional

import pluggy

from athena.models.data_parser_plugin import DataParserPlugin
from athena.plugins.builtin import BUILTIN_PARSER_PLUGINS
from athena.plugins.hookspecs import DataParserHooks


class DataParserPluginsManager:
    """Manager for data parser plugins."""

    def __init__(self, project_name: str) -> None:
        """Initialize the data parser plugins manager.

        Args:
            project_name: The name of the project
        """
        self.parsers: Dict[str, DataParserPlugin] = {}
        self.logger = logging.getLogger(__name__)
        self.pm = pluggy.PluginManager(project_name)
        self.pm.add_hookspecs(DataParserHooks)

    def load_builtin_plugins(self) -> None:
        """Register essential plugins from the built-in registry."""
        for plugin in BUILTIN_PARSER_PLUGINS:
            self.logger.debug(f"Registering built-in plugin: {plugin.__name__}")
            self.pm.register(plugin)

    def load_entrypoint_plugins(self, entrypoint_name: str) -> None:
        """Load plugins from setuptools entrypoints."""
        try:
            self.pm.load_setuptools_entrypoints(entrypoint_name)
            self.logger.info(f"Loaded plugins from entrypoint: {entrypoint_name}")
        except Exception as e:
            self.logger.error(f"Failed to load entrypoint plugins: {e}")

    def load_plugins(self) -> None:
        """Load all data parser plugins."""
        available_parsers: List[DataParserPlugin] = (
            self.pm.hook.register_data_parser_plugin()
        )
        for parser in available_parsers:
            self.logger.debug(
                f'Loading data parser "{parser.metadata.name}" for supported formats "{parser.supported_formats}"'
            )
            for ext in parser.supported_formats:
                self.parsers[ext] = parser

    def get_parser(self, format: str) -> Optional[DataParserPlugin]:
        """Get a parser by format.

        Args:
            format: The format/extension to get a parser for

        Returns:
            The data parser plugin or None if not found
        """
        if format not in self.parsers:
            return None
        return self.parsers[format]

    def parse_data(self, data: str, format: str) -> Optional[Dict[str, Any]]:
        """Parse data using the appropriate parser.

        Args:
            data: The data to parse
            format: The format of the data

        Returns:
            The parsed data or None if no parser is found
        """
        parser = self.get_parser(format)
        if not parser:
            self.logger.warning(f"No parser found for format '{format}'")
            return None

        return parser.parser.parse(data)

    @property
    def supported_formats(self) -> List[str]:
        """Get a list of all supported formats.

        Returns:
            List of supported format extensions
        """
        return list(self.parsers.keys())
