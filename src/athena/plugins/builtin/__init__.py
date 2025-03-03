"""Built-in plugins for Athena."""

from types import ModuleType
from typing import List
from athena.plugins.builtin.data_parsers import json_data_parser, yaml_data_parser
from athena.plugins.builtin.test_runners import system_test_runner
from athena.plugins.builtin.reporters import json_reporter

BUILTIN_PARSER_PLUGINS: List[ModuleType] = [
    yaml_data_parser,
    json_data_parser,
]

BUILTIN_TEST_RUNNER_PLUGINS: List[ModuleType] = [
    system_test_runner,
]

BUILTIN_REPORTER_PLUGINS: List[ModuleType] = [
    json_reporter,
]
