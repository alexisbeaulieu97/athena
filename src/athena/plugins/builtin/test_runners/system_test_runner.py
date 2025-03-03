from typing import Any
from athena.models.test_plugin import TestPlugin
from athena.models.plugin_metadata import PluginMetadata
from athena.models.test_result import TestResult
from athena.models.test_details import TestDetails
import psutil
from athena.plugins import hookimpl
from athena.models.test_passed_result import TestPassedResult
from athena.models.test_failed_result import TestFailedResult
from athena.models.test_skipped_result import TestSkippedResult


@hookimpl(tryfirst=True)
def register_test_plugin() -> TestPlugin:
    return TestPlugin(
        metadata=PluginMetadata(
            name="system",
            description="A plugin to collect system information",
        ),
        runner=SystemTestRunner(),
    )


class SystemTestRunner:
    def run(self, **kwargs: Any) -> TestResult:
        details: dict[str, TestDetails] = {}
        if "cpu" in kwargs:
            details["cpu"] = TestDetails(
                expected=kwargs.get("cpu", {}).get("threshold", 80),
                actual=psutil.cpu_percent(interval=1),
                success=(
                    kwargs.get("cpu", {}).get("threshold", 80)
                    > psutil.cpu_percent(interval=1)
                ),
            )
        if "memory" in kwargs:
            details["memory"] = TestDetails(
                expected=kwargs.get("memory", {}).get("threshold", 80),
                actual=psutil.virtual_memory().percent,
                success=(
                    kwargs.get("memory", {}).get("threshold", 80)
                    > psutil.virtual_memory().percent
                ),
            )
        if "disk" in kwargs:
            details["disk"] = TestDetails(
                expected=kwargs.get("disk", {}).get("threshold", 80),
                actual=psutil.disk_usage(kwargs["disk"]["path"]).percent,
                success=(
                    kwargs.get("disk", {}).get("threshold", 80)
                    > psutil.disk_usage(kwargs["disk"]["path"]).percent
                ),
            )

        if not details:
            return TestSkippedResult(
                message="No system checks configured.",
            )
        if all(result.success for result in details.values()):
            return TestPassedResult(
                details=details,
            )
        else:
            return TestFailedResult(
                details=details,
            )
