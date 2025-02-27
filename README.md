# Athena Test Framework

A flexible testing framework with a plugin architecture for configuration, test execution, and reporting.

## Features

- Plugin-based architecture allows for easy extension
- Multiple configuration formats (YAML, JSON)
- Configurable test parameters
- Multiple reporting formats (Console, JSON)
- Detailed test results with timing and status information

## Installation

```bash
pip install athena-test-framework
```

## Usage

Basic usage with default configuration:

```bash
python -m athena.cli run config.yml
```

With custom config and report formats:

```bash
python -m athena.cli run config.json --config-format json --report-format json
```

## Configuration

Athena supports configuration files in YAML (default) or JSON format. You can specify multiple tests to run along with their parameters.

### Example Configuration

```yaml
# Global parameters (applied to all tests unless overridden)
timeout: 30  # Default timeout in seconds for all tests
retry_count: 2  # Number of retries for failed tests

# List of tests to run with their specific parameters
tests:
  - name: system_info
    parameters:
      collect_network: true  # Enable network information collection
  
  - name: memory_check
    parameters:
      memory_threshold: 75  # Override the default memory threshold (90%)

# You can add more global parameters here
environment: "production"
log_level: "info"
```

## Available Tests

### System Tests

- `system_info`: Collects basic system information
  - Parameters:
    - `collect_network`: Whether to include network interface information (default: false)

- `memory_check`: Verifies system memory usage is below threshold
  - Parameters:
    - `memory_threshold`: Maximum memory usage percentage (default: 90)

## Extending

Athena can be extended with plugins for:
- New test types
- Alternative configuration formats
- Custom reporting formats

See the plugin documentation for details on creating custom plugins.