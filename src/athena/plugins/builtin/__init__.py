"""Built-in plugins for Athena."""

from typing import List, Type
from athena.plugins.builtin import system_info_test, yaml_plugin

BUILTIN_PLUGINS: List[Type] = [
    yaml_plugin,
    system_info_test,
]
