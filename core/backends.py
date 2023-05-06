from abc import ABC, abstractmethod
from typing import List

from core.enums import DatastoreStatus
from core.result import Result


class Backend(ABC):
    @abstractmethod
    def set(self, key: str, value: str) -> Result:
        """
        Set the value of the given key to the provided value. Creates an entry if it doesn't exist.

        Args:
            key (str): The key to set.
            value (str): The value to set.

        Returns:
            Result: A Result instance with the status of the operation.
        """
        pass

    @abstractmethod
    def get(self, key: str) -> str | Result:
        """
        Get the value of the given key.

        Args:
            key (str): The key to get the value for.

        Returns:
            str | Result: The value of the key if found, or a Result instance with the status of the operation
                          if an error occurs.
        """
        pass

    @abstractmethod
    def delete(self, key: str) -> Result:
        """
        Delete the entry for the given key.

        Args:
            key (str): The key to delete.

        Returns:
            Result: A Result instance with the status of the operation.
        """
        pass

    @abstractmethod
    def keys(self) -> List[str] | Result:
        """
        Get a list of all keys in the datastore.

        Returns:
            List[str] | Result: A list of all keys in the datastore, or a Result instance with the status of the
                                operation if an error occurs.
        """
        pass


class InMemoryBackend(Backend):

    def __init__(self):
        self.storage = {}

    def set(self, key: str, value: str) -> Result:
        try:
            self.storage[key] = value
            return Result(DatastoreStatus.OK)
        except Exception as e:
            return Result(DatastoreStatus.ERROR, str(e))

    def get(self, key: str) -> str | Result:
        try:
            return self.storage.get(key, None)
        except Exception as e:
            return Result(DatastoreStatus.ERROR, str(e))

    def delete(self, key: str) -> Result:
        try:
            if key in self.storage:
                del self.storage[key]
            else:
                return Result(DatastoreStatus.KEY_NOT_FOUND, "Key not found")
            return Result(DatastoreStatus.OK)
        except Exception as e:
            return Result(DatastoreStatus.ERROR, str(e))

    def keys(self) -> List[str] | Result:
        try:
            return list(self.storage.keys())
        except Exception as e:
            return Result(DatastoreStatus.ERROR, str(e))
