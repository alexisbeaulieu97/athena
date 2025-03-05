from typing import Any, Optional

from athena.models import BaseModel
from athena.models.reporter_config import ReporterConfig
from athena.models.test_config import TestConfig


class TestSuiteConfig(BaseModel):
    """Model representing the configuration of a test suite."""

    parameters: Optional[dict[str, Any]]
    tests: list[TestConfig]
    reports: list[ReporterConfig]
