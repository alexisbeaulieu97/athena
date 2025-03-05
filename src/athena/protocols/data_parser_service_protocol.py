from typing import Protocol, runtime_checkable


@runtime_checkable
class DataParserServiceProtocol(Protocol):
    """Protocol defining the interface for data parser services."""

    def parse_data(self, data):
        """Parse the data and return the result."""
        ...
