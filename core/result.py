from typing import Any

from core.enums import DatastoreStatus


class Result:
    """
    A result from a datastore operation.
    """

    def __init__(self, status: DatastoreStatus, message: str | None = None, value: Any = None):
        """
        Initialize the result.

        Attributes:
            status (DatastoreError): The status of the operation.
            message (str): A message describing the result.
            value (Any): The value of the result.
        """
        self.status = status
        self.message = message
        self.value = value

    def is_successful(self):
        """
        Check if the result is a success.
        """
        return self.status == DatastoreStatus.OK or self.status == DatastoreStatus.IN_TRANSACTION_LIST

    def __str__(self):
        if self.value:
            return self.value

        if not self.message:
            return f"Status: {self.status.name}"

        return f"Status: {self.status.name}, Message: {self.message}"
