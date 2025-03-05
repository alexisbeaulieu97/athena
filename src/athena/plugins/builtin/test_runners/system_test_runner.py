from typing import Any

import psutil

from athena.models import BaseModel
from athena.models.plugin import Plugin
from athena.models.plugin_metadata import PluginMetadata
from athena.models.test_details import TestDetails
from athena.models.test_result import TestResult
from athena.plugins import hookimpl
from athena.types import TestRunnerPluginResult


class SystemTestRunnerParameters(BaseModel):
    cpu: dict[str, Any] = {}
    memory: dict[str, Any] = {}
    disk: dict[str, Any] = {}


@hookimpl
def activate_test_plugin() -> Plugin[
    TestRunnerPluginResult,
    SystemTestRunnerParameters,
]:
    return Plugin(
        metadata=PluginMetadata(
            name="system",
            description="A plugin to collect system information",
        ),
        executor=SystemTestRunner(),
        parameters_model=SystemTestRunnerParameters,
        identifiers={"system"},
    )


class SystemTestRunner:
    def __call__(
        self, parameters: SystemTestRunnerParameters
    ) -> TestRunnerPluginResult:
        details: dict[str, TestDetails] = {}
        if parameters.cpu:
            details["cpu"] = TestDetails(
                expected=parameters.cpu.get("threshold", 80),
                actual=psutil.cpu_percent(interval=1),
                success=(
                    parameters.cpu.get("threshold", 80) > psutil.cpu_percent(interval=1)
                ),
            )
        if parameters.memory:
            details["memory"] = TestDetails(
                expected=parameters.memory.get("threshold", 80),
                actual=psutil.virtual_memory().percent,
                success=(
                    parameters.memory.get("threshold", 80)
                    > psutil.virtual_memory().percent
                ),
            )
        if parameters.disk:
            details["disk"] = TestDetails(
                expected=parameters.disk.get("threshold", 80),
                actual=psutil.disk_usage(parameters.disk["path"]).percent,
                success=(
                    parameters.disk.get("threshold", 80)
                    > psutil.disk_usage(parameters.disk["path"]).percent
                ),
            )

        if not details:
            return TestResult.skipped(
                message="No system checks configured.",
            )
        if all(result.success for result in details.values()):
            return TestResult.passed(
                details=details,
            )
        else:
            return TestResult.failed(
                details=details,
            )
