"""Built-in plugins for Athena."""

from typing import List, Type
from athena.plugins.builtin import system_info_test, yaml_plugin, json_summary

BUILTIN_PLUGINS: List[Type] = [
    yaml_plugin,
    system_info_test,
    json_summary,
]
