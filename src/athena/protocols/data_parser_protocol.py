from typing import Any, Optional
from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class DataParserProtocol(Protocol):
    def parse(
        self,
        data: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Parse raw string data into a dictionary.

        Args:
            data: The raw data as a string

        Returns:
            Parsed dict
        """
        ...
