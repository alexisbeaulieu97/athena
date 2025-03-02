from typing import Any
from athena.models import (
    PluginMetadata,
    TestDetails,
    TestFailedResult,
    TestPlugin,
    TestPassedResult,
    TestResult,
    TestSkippedResult,
)
import psutil
from athena.plugins import hookimpl


@hookimpl
def register_test() -> TestPlugin:
    return TestPlugin(
        metadata=PluginMetadata(
            name="system",
            version="0.1.0",
            description="A plugin to collect system information",
        ),
        test=test,
    )


def test(config: dict[str, Any]) -> TestResult:
    details: dict[str, TestDetails] = {}
    if "cpu" in config:
        details["cpu"] = TestDetails(
            expected=config.get("cpu", {}).get("threshold", 80),
            actual=psutil.cpu_percent(interval=1),
            success=(
                config.get("cpu", {}).get("threshold", 80)
                > psutil.cpu_percent(interval=1)
            ),
        )
    if "memory" in config:
        details["memory"] = TestDetails(
            expected=config.get("memory", {}).get("threshold", 80),
            actual=psutil.virtual_memory().percent,
            success=(
                config.get("memory", {}).get("threshold", 80)
                > psutil.virtual_memory().percent
            ),
        )
    if "disk" in config:
        details["disk"] = TestDetails(
            expected=config.get("disk", {}).get("threshold", 80),
            actual=psutil.disk_usage(config["disk"]["path"]).percent,
            success=(
                config.get("disk", {}).get("threshold", 80)
                > psutil.disk_usage(config["disk"]["path"]).percent
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
