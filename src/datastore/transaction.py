# Builtin
import queue
# Internal
from src.datastore.types.datastore_operation import DatastoreOperations


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
                datastore.update(key, value, is_transaction=True)
            elif change_type == DatastoreOperations.DELETE:
                datastore.insert(key, value, is_transaction=True)
