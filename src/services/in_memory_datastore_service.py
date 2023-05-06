# Builtin
from functools import wraps
from typing import List, Callable
# Internal
from src.datastore.datastore_result import Result
from src.datastore.types.datastore_status import DatastoreStatus
from src.services.service import Backend


def exception_handler(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return Result(DatastoreStatus.ERROR, str(e))

    return wrapper


class InMemoryBackend(Backend):
    def __init__(self):
        self.storage = {}

    @exception_handler
    def set(self, key: str, value: str) -> Result:
        self.storage[key] = value
        return Result(DatastoreStatus.OK)

    @exception_handler
    def get(self, key: str) -> str | Result:
        return self.storage.get(key, None)

    @exception_handler
    def delete(self, key: str) -> Result:
        if key in self.storage:
            del self.storage[key]
            return Result(DatastoreStatus.OK)
        else:
            return Result(DatastoreStatus.KEY_NOT_FOUND, "Key not found")

    @exception_handler
    def keys(self) -> List[str] | Result:
        return list(self.storage.keys())
