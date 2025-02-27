import platform
import time
from typing import Any, Dict

import psutil

from athena.models import TestResult, TestStatus
from athena.plugins import hookimpl


class SystemTestPlugin:
    NAME = "system_test"
    VERSION = "1.0.0"

    # Define available tests with their default parameters
    AVAILABLE_TESTS = {
        "system_info": {
            "description": "Collects basic system information",
            "parameters": {
                "collect_network": {
                    "type": "boolean",
                    "description": "Whether to collect network interface information",
                    "default": False
                }
            }
        },
        "memory_check": {
            "description": "Checks if memory usage is below the specified threshold",
            "parameters": {
                "memory_threshold": {
                    "type": "integer",
                    "description": "Memory usage threshold percentage",
                    "default": 90
                }
            }
        }
    }

    @hookimpl
    def athena_run_test(self, name: str, config: Dict[str, Any]) -> TestResult:
        start_time = time.time()

        if name == "system_info":
            try:
                # Get the collect_network parameter with default
                collect_network = config.get("collect_network", False)

                system_info = {
                    "os": platform.system(),
                    "python_version": platform.python_version(),
                    "cpu_count": psutil.cpu_count(),
                    "memory_total": psutil.virtual_memory().total,
                    "memory_available": psutil.virtual_memory().available,
                }

                # Add network info if requested
                if collect_network:
                    try:
                        # Simple network info collection
                        network_info = {}
                        for interface, stats in psutil.net_if_stats().items():
                            network_info[interface] = {
                                "up": stats.isup,
                                "speed": stats.speed,
                                "mtu": stats.mtu
                            }
                        system_info["network"] = network_info
                    except Exception as e:
                        system_info["network_error"] = str(e)

                return TestResult(
                    plugin_name=self.NAME,
                    test_name=name,
                    test_version=self.VERSION,
                    duration=time.time() - start_time,
                    status=TestStatus.SUCCESS,
                    message="System information collected successfully",
                    details=system_info
                )
            except Exception as e:
                return TestResult(
                    plugin_name=self.NAME,
                    test_name=name,
                    test_version=self.VERSION,
                    duration=time.time() - start_time,
                    status=TestStatus.ERROR,
                    message=f"Failed to collect system information: {str(e)}"
                )

        elif name == "memory_check":
            try:
                memory = psutil.virtual_memory()
                memory_usage = memory.percent
                threshold = config.get("memory_threshold", 90)

                if memory_usage > threshold:
                    status = TestStatus.FAILED
                    message = f"Memory usage ({memory_usage}%) exceeds threshold ({threshold}%)"
                else:
                    status = TestStatus.SUCCESS
                    message = f"Memory usage ({memory_usage}%) is within acceptable range"

                return TestResult(
                    plugin_name=self.NAME,
                    test_name=name,
                    test_version=self.VERSION,
                    duration=time.time() - start_time,
                    status=status,
                    message=message,
                    details={"usage": memory_usage, "threshold": threshold}
                )
            except Exception as e:
                return TestResult(
                    plugin_name=self.NAME,
                    test_name=name,
                    test_version=self.VERSION,
                    duration=time.time() - start_time,
                    status=TestStatus.ERROR,
                    message=f"Failed to check memory: {str(e)}"
                )

        return TestResult(
            plugin_name=self.NAME,
            test_name=name,
            test_version=self.VERSION,
            duration=time.time() - start_time,
            status=TestStatus.SKIPPED,
            message=f"Test '{name}' not found in plugin"
        )

    @hookimpl
    def athena_register_test(self) -> Dict[str, Any]:
        return {
            "name": self.NAME,
            "version": self.VERSION,
            "description": "System information and resource usage tests",
            "dependencies": ["psutil>=7.0.0"],
            "available_tests": self.AVAILABLE_TESTS
        }
