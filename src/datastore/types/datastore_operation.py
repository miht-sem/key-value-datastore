# Builtin
from enum import Enum


class DatastoreOperations(Enum):
    INSERT = 'insert'
    UPDATE = 'update'
    SELECT = 'select'
    DELETE = 'delete'
