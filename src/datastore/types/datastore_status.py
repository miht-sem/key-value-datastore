# Builtin
from enum import Enum, auto


class DatastoreStatus(Enum):
    OK = auto()
    KEY_NOT_FOUND = auto()
    KEY_ALREADY_EXISTS = auto()
    TRANSACTION_ALREADY_IN_PROGRESS = auto()
    IN_TRANSACTION_LIST = auto()
    NO_TRANSACTION_IN_PROGRESS = auto()
    ERROR = auto()
