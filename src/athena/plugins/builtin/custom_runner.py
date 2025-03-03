"""Example of a custom test runner using the Protocol-based interface.

This module demonstrates how to create a custom test runner that implements
the TestRunnerProtocol without using the plugin hook system.
"""

import platform
import psutil
from typing import Dict, Any, Optional

from athena.models import (
    PluginMetadata,
    TestConfig,
    TestDetails,
    TestFailedResult,
    TestPassedResult,
    TestResult,
    TestRunnerProtocol,
    TestSkippedResult,
)


class MemoryTestRunner(TestRunnerProtocol):
    """Test runner for memory usage tests."""

    def __init__(self):
        """Initialize the memory test runner."""
        self.metadata = PluginMetadata(
            name="memory",
            version="1.0.0",
            description="Test runner for memory usage tests",
        )

    def run(self, config: TestConfig) -> TestResult:
        """Run memory usage tests.

        Args:
            config: Test configuration

        Returns:
            Test result
        """
        # Extract parameters with defaults
        threshold = config.parameters.get("threshold", 80)  # Default to 80%
        warning_level = config.parameters.get("warning_level", 60)  # Default to 60%

        # Skip if test is not configured
        if threshold is None:
            return TestSkippedResult(message="Memory test not configured")

        # Get system memory info
        memory = psutil.virtual_memory()
        memory_percent = memory.percent

        details = {
            "memory_usage": TestDetails(
                expected=f"< {threshold}%",
                actual=f"{memory_percent:.1f}%",
                success=memory_percent < threshold,
            )
        }

        # Check warning level
        if (
            warning_level
            and memory_percent >= warning_level
            and memory_percent < threshold
        ):
            return TestPassedResult(
                message=f"Memory usage is high but within limits: {memory_percent:.1f}%",
                details=details,
            )

        # Check failure level
        if memory_percent >= threshold:
            return TestFailedResult(
                message=f"Memory usage exceeds threshold: {memory_percent:.1f}% >= {threshold}%",
                details=details,
            )

        # All checks passed
        return TestPassedResult(
            message=f"Memory usage is within limits: {memory_percent:.1f}%",
            details=details,
        )


class DiskTestRunner(TestRunnerProtocol):
    """Test runner for disk usage tests."""

    def __init__(self):
        """Initialize the disk test runner."""
        self.metadata = PluginMetadata(
            name="disk",
            version="1.0.0",
            description="Test runner for disk usage tests",
        )

    def run(self, config: TestConfig) -> TestResult:
        """Run disk usage tests.

        Args:
            config: Test configuration

        Returns:
            Test result
        """
        # Extract parameters with defaults
        path = config.parameters.get("path", "/")  # Default to root path
        threshold = config.parameters.get("threshold", 90)  # Default to 90%

        # Skip if test is not configured
        if threshold is None:
            return TestSkippedResult(message="Disk test not configured")

        # Get disk usage info
        disk = psutil.disk_usage(path)
        disk_percent = disk.percent

        details = {
            "disk_usage": TestDetails(
                expected=f"< {threshold}%",
                actual=f"{disk_percent:.1f}%",
                success=disk_percent < threshold,
            )
        }

        # Check failure level
        if disk_percent >= threshold:
            return TestFailedResult(
                message=f"Disk usage exceeds threshold: {disk_percent:.1f}% >= {threshold}%",
                details=details,
            )

        # All checks passed
        return TestPassedResult(
            message=f"Disk usage is within limits: {disk_percent:.1f}%",
            details=details,
        )


# These instances can be directly used without the plugin manager
memory_runner = MemoryTestRunner()
disk_runner = DiskTestRunner()


# Factory function to get all runners
def get_runners():
    """Get all test runners defined in this module.

    Returns:
        Dictionary mapping runner names to instances
    """
    return {
        "memory": memory_runner,
        "disk": disk_runner,
    }
