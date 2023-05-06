# Builtin
import queue
import re
from typing import Any, List
# Internal
from src.datastore.datastore_result import Result
from src.datastore.types.datastore_operation import DatastoreOperations
from src.datastore.types.datastore_status import DatastoreStatus
from src.services.in_memory_datastore_service import InMemoryBackend


class Transaction:
    """
    A transaction for the datastore.
    """

    def __init__(self):
        self.operations = queue.Queue()
        self.changes = []

    def insert(self, key: str, value: str):
        self.operations.put((DatastoreOperations.INSERT, key, value))

    def update(self, key: str, value: str):
        self.operations.put((DatastoreOperations.UPDATE, key, value))

    def select(self, key: str):
        self.operations.put((DatastoreOperations.SELECT, key))

    def delete(self, key: str):
        self.operations.put((DatastoreOperations.DELETE, key))

    def add_change(self, change_type: DatastoreOperations, key: str, value=None):
        self.changes.append((change_type, key, value))

    def rollback_changes(self, datastore):
        while self.changes:
            change_type, key, value = self.changes.pop()
            if change_type == DatastoreOperations.INSERT:
                datastore.delete(key, is_transaction=True)
            elif change_type == DatastoreOperations.UPDATE:
                datastore.set(key, value, is_transaction=True)
            elif change_type == DatastoreOperations.DELETE:
                datastore.set(key, value, is_transaction=True)


class Datastore:
    """
    A datastore that stores key-value pairs.
    """

    def __init__(self, backend=None, in_memory=False):
        """
        Initialize the datastore.

        Args:
            backend (Backend): The backend to use for the datastore. If None, an in-memory backend will be used.
            in_memory (bool): Whether to use an in-memory backend. If True, backend will be ignored.

        Raises:
            ValueError: If backend is None and in_memory is False.
        """

        if backend is None and not in_memory:
            raise ValueError("backend cannot be None if in_memory is False")

        self.in_memory = in_memory
        self.backend = backend if not in_memory else InMemoryBackend()
        self.transactions = None

    def insert(self, key: str, value: str, is_transaction=False) -> Result:
        """
        Create a new entry for the given key with the provided value.

        Args:
            key (str): The key for the entry.
            value (str): The value for the entry.
            is_transaction (bool): Whether the "insert" is part of a transaction.

        Returns:
            Result: A Result instance with the status of the operation.
        """

        if self.transactions and not is_transaction:
            self.transactions.insert(key, value)
            return Result(DatastoreStatus.IN_TRANSACTION_LIST)

        if self.backend.get(key) is not None:
            return Result(DatastoreStatus.KEY_ALREADY_EXISTS, "Key already exists")

        result = self.backend.set(key, value)
        if not result.is_successful():
            return result

        return Result(DatastoreStatus.OK)

    def update(self, key: str, value: str, is_transaction=False) -> Result:
        """
        Update the value of the given key with the provided value.

        Args:
            key (str): The key for the entry.
            value (str): The new value for the entry.
            is_transaction (bool): Whether the "update" is part of a transaction.

        Returns:
            Result: A Result instance with the status of the operation.
        """

        if self.transactions and not is_transaction:
            self.transactions.update(key, value)
            return Result(DatastoreStatus.IN_TRANSACTION_LIST)

        if self.backend.get(key) is None:
            return Result(DatastoreStatus.KEY_NOT_FOUND, "Key not found")

        result = self.backend.set(key, value)
        if not result.is_successful():
            return result

        return Result(DatastoreStatus.OK)

    def select(self, key: str, is_transaction=False) -> Result:
        """
        Get the value of the given key.

        Args:
            key (str): The key to get the value for.
            is_transaction (bool): Whether the "select" is part of a transaction.

        Returns:
            Result: A Result instance with the status of the operation and the value of the key if found.
        """

        if self.transactions and not is_transaction:
            self.transactions.select(key)
            return Result(DatastoreStatus.IN_TRANSACTION_LIST)

        value = self.backend.get(key)
        if value is None:
            return Result(DatastoreStatus.KEY_NOT_FOUND, "Key not found")
        return Result(DatastoreStatus.OK, value=value)

    def delete(self, key: str, is_transaction=False) -> Result:
        """
        Delete the entry for the given key.

        Args:
            key (str): The key to delete.
            is_transaction (bool): Whether the "delete" is part of a transaction.

        Returns:
            Result: A Result instance with the status of the operation.
        """

        if self.transactions and not is_transaction:
            self.transactions.delete(key)
            return Result(DatastoreStatus.IN_TRANSACTION_LIST)

        result = self.backend.delete(key)
        if not result.is_successful():
            return result

        return Result(DatastoreStatus.OK)

    def begin(self) -> Result:
        """
        Begin a new transaction.

        Returns:
            Result: A Result instance with the status of the operation.
        """

        if self.transactions:
            return Result(DatastoreStatus.TRANSACTION_ALREADY_IN_PROGRESS, "Transaction already in progress")

        self.transactions = Transaction()

        return Result(DatastoreStatus.OK)

    def commit(self) -> Result:
        """
        Commit the current transaction.

        Returns:
            Result: A Result instance with the status of the operation.
        """

        if not self.transactions:
            return Result(DatastoreStatus.NO_TRANSACTION_IN_PROGRESS, "No transaction in progress")

        try:
            while not self.transactions.operations.empty():
                operation, key, value = self.transactions.operations.get()
                result = Result(DatastoreStatus.ERROR)
                if operation == operation.INSERT:
                    result = self.insert(key, value, True)
                elif operation == operation.UPDATE:
                    result = self.update(key, value, True)
                elif operation == operation.SELECT:
                    result = self.select(key, True)
                elif operation == operation.DELETE:
                    result = self.delete(key, True)

                if not result.is_successful():
                    self.rollback()
                    return result
                else:
                    self.transactions.add_change(operation, key, value)

        except Exception as e:
            self.rollback()
            return Result(DatastoreStatus.ERROR, str(e))

        self.transactions = None

        return Result(DatastoreStatus.OK)

    def rollback(self) -> Result:
        """
        Rollback the current transaction.

        Returns:
            Result: A Result instance with the status of the operation.
        """
        if not self.transactions:
            return Result(DatastoreStatus.NO_TRANSACTION_IN_PROGRESS, "No transaction in progress")

        self.transactions.rollback_changes(self)
        self.transactions = None
        return Result(DatastoreStatus.OK)

    def keys(self, pattern: str) -> List[Any] | Result:
        """
        Get a list of keys matching the given pattern.

        Args:
            pattern (str): The pattern to match keys against.

        Returns:
            List[Any] | Result: A list of keys that match the pattern, or a Result instance with the status of
                                the operation if an error occurs.
        """
        try:
            keys = self.backend.keys()
            matched_keys = [key for key in keys if re.match(pattern, key)]
            return matched_keys
        except Exception as e:
            return Result(DatastoreStatus.ERROR, str(e))
