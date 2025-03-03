# Creating Plugins for Athena

This guide explains how to create plugins for the Athena testing framework using the Protocol-based plugin architecture.

## Overview

Athena now supports a flexible, protocol-based plugin architecture that allows you to:

1. Create plugins using Python's Protocol typing for structural interfaces
2. Distribute plugins as standalone packages via pip
3. Register plugins using setuptools entrypoints
4. Mix and match different plugin components (parsers, runners, reporters)

## Plugin Types

Plugins can implement any of the following interfaces:

- `ConfigParserProtocol`: For parsing configuration data
- `TestRunnerProtocol`: For running tests
- `ReporterProtocol`: For generating reports from test results

## Creating a Plugin

### Option 1: Direct Protocol Implementation

The simplest way to create a plugin is to implement the protocol interfaces directly:

```python
from athena.models import TestRunnerProtocol, TestConfig, TestResult, TestPassedResult

class MyTestRunner(TestRunnerProtocol):
    def run(self, config: TestConfig) -> TestResult:
        # Implement your test logic here
        return TestPassedResult(message="Test passed")
```

### Option 2: Plugin Provider

For more complex plugins that provide multiple components, create a provider:

```python
from athena.interfaces import PluginProviderProtocol

class MyPluginProvider:
    def get_parsers(self):
        return [MyParser()]

    def get_runners(self):
        return {"my-test": MyTestRunner()}

    def get_reporters(self):
        return [MyReporter()]
```

### Option 3: Legacy Hook-based Plugins

For backward compatibility, you can still create plugins using the hook-based approach:

```python
from athena.plugins import hookimpl

@hookimpl
def register_test():
    return TestPlugin(...)

@hookimpl
def parse_raw_data(data, format=None):
    if format == "my-format":
        return parse_data(data)
    return None
```

## Distributing Plugins

### 1. Create a Package Structure

```
my-athena-plugin/
├── my_plugin/
│   ├── __init__.py
│   ├── plugin.py
│   └── reporters.py
├── pyproject.toml
└── README.md
```

### 2. Implement Your Plugin

In `plugin.py`:

```python
from athena.models import TestRunnerProtocol, TestConfig, TestResult

class MyTestRunner(TestRunnerProtocol):
    def run(self, config: TestConfig) -> TestResult:
        # Your test logic here
        ...

def create_plugin():
    return MyTestRunner()
```

### 3. Configure Entry Points

In your `pyproject.toml`:

```toml
[project.entry-points."athena.plugins"]
my-plugin = "my_plugin.plugin:create_plugin"
```

Or in `setup.py`:

```python
setup(
    # ...
    entry_points={
        "athena.plugins": [
            "my-plugin=my_plugin.plugin:create_plugin",
        ],
    },
)
```

### 4. Install and Use

Once installed, your plugin will be automatically discovered and loaded by Athena:

```bash
pip install my-athena-plugin
athena run my-config.yml
```

## Advanced Usage

### Combining Multiple Plugins

Your plugin provider can implement multiple interfaces:

```python
class MyProvider:
    def get_parsers(self):
        return [XmlParser(), JsonParser()]

    def get_runners(self):
        return {
            "network": NetworkTestRunner(),
            "performance": PerformanceTestRunner(),
        }

    def get_reporters(self):
        return [HtmlReporter(), JsonReporter()]
```

### Conditional Plugin Behavior

You can implement dynamic plugin behavior:

```python
def create_plugin():
    # Choose components based on environment, configuration, etc.
    if os.environ.get("ATHENA_DEBUG"):
        return DebugPluginProvider()
    return StandardPluginProvider()
```

## Protocol Interfaces

For reference, here are the key protocols your plugins should implement:

```python
@runtime_checkable
class ConfigParserProtocol(Protocol):
    def parse(self, data: str, format: Optional[str] = None) -> Optional[Dict[str, Any]]:
        ...

@runtime_checkable
class TestRunnerProtocol(Protocol):
    def run(self, config: TestConfig) -> TestResult:
        ...

@runtime_checkable
class ReporterProtocol(Protocol):
    def report(self, summary: TestSuiteSummary) -> None:
        ...

@runtime_checkable
class PluginProviderProtocol(Protocol):
    def get_parsers(self) -> List[ConfigParserProtocol]:
        ...

    def get_runners(self) -> Dict[str, TestRunnerProtocol]:
        ...

    def get_reporters(self) -> List[ReporterProtocol]:
        ...
```

For more detailed examples, see the `examples/plugin_example.py` file in the Athena repository.
