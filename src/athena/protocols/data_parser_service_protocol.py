from typing import Generic, Protocol, TypeVar, runtime_checkable

DataType = TypeVar("DataType", contravariant=True)
ResultType = TypeVar("ResultType", covariant=True)


@runtime_checkable
class DataParserServiceProtocol(Protocol, Generic[DataType, ResultType]):
    """Protocol defining the interface for data parser services."""

    def parse_data(self, data: DataType) -> ResultType:
        """Parse the data and return the result."""
        ...
