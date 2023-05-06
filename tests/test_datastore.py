# Builtin
import unittest

# Internal
from src.datastore.datastore import Datastore
from src.datastore.types.datastore_status import DatastoreStatus


class TestPrintDatastore(unittest.TestCase):
    def setUp(self):
        # this line is important
        self.datastore = Datastore(in_memory=True)

    def test_insert(self):
        result = self.datastore.insert("key1", "value1")
        self.assertEqual(result.status, DatastoreStatus.OK)

        result = self.datastore.insert("key1", "value2")
        self.assertEqual(result.status, DatastoreStatus.KEY_ALREADY_EXISTS)

    def test_update(self):
        self.datastore.insert("key1", "value1")
        result = self.datastore.update("key1", "value2")
        self.assertEqual(result.status, DatastoreStatus.OK)

    def test_select(self):
        self.datastore.insert("key1", "value1")
        result = self.datastore.select("key1")
        self.assertEqual(result.value, "value1")

        result = self.datastore.select("nonexistent_key")
        self.assertEqual(result.status, DatastoreStatus.KEY_NOT_FOUND)

    def test_delete(self):
        self.datastore.insert("key1", "value1")
        result = self.datastore.delete("key1")
        self.assertEqual(result.status, DatastoreStatus.OK)

        result = self.datastore.delete("key1")
        self.assertEqual(result.status, DatastoreStatus.KEY_NOT_FOUND)

    def test_transactions_OK(self):
        result = self.datastore.begin()
        self.assertEqual(result.status, DatastoreStatus.OK)

        result = self.datastore.insert("key2", "value1")
        self.assertEqual(result.status, DatastoreStatus.IN_TRANSACTION_LIST)

        result = self.datastore.update("key2", "value2")
        self.assertEqual(result.status, DatastoreStatus.IN_TRANSACTION_LIST)

        result = self.datastore.commit()
        self.assertEqual(result.status, DatastoreStatus.OK)

        result = self.datastore.select("key2")
        self.assertEqual(result.value, "value2")

    def test_transactions_rollback_INSERT(self):

        result = self.datastore.begin()
        self.assertEqual(result.status, DatastoreStatus.OK)

        result = self.datastore.insert("key3", "value1")
        self.assertEqual(result.status, DatastoreStatus.IN_TRANSACTION_LIST)

        result = self.datastore.update("nonexistent_key", "value")
        self.assertEqual(result.status, DatastoreStatus.IN_TRANSACTION_LIST)

        result = self.datastore.commit()
        self.assertEqual(result.status, DatastoreStatus.KEY_NOT_FOUND)

        result = self.datastore.select("key3")
        self.assertEqual(result.status, DatastoreStatus.KEY_NOT_FOUND)

    def test_transactions_rollback_DELETE(self):

        result = self.datastore.insert("key4", "value1")
        self.assertEqual(result.status, DatastoreStatus.OK)

        result = self.datastore.begin()
        self.assertEqual(result.status, DatastoreStatus.OK)

        result = self.datastore.delete("key4")
        self.assertEqual(result.status, DatastoreStatus.IN_TRANSACTION_LIST)

        result = self.datastore.delete("key234")
        self.assertEqual(result.status, DatastoreStatus.IN_TRANSACTION_LIST)

        result = self.datastore.commit()
        self.assertEqual(result.status, DatastoreStatus.ERROR)

        result = self.datastore.select("key4")
        self.assertEqual(result.value, "value1")

    def test_transactions_rollback_UPDATE(self):

        result = self.datastore.insert("key5", "value1")
        self.assertEqual(result.status, DatastoreStatus.OK)

        result = self.datastore.begin()
        self.assertEqual(result.status, DatastoreStatus.OK)

        result = self.datastore.update("key5", "value2")
        self.assertEqual(result.status, DatastoreStatus.IN_TRANSACTION_LIST)

        result = self.datastore.delete("key234")
        self.assertEqual(result.status, DatastoreStatus.IN_TRANSACTION_LIST)

        result = self.datastore.commit()
        self.assertEqual(result.status, DatastoreStatus.ERROR)

        result = self.datastore.select("key5")
        self.assertEqual(result.value, "value1")

    def test_keys_pattern(self):
        self.datastore.insert("key1", "value1")
        self.datastore.insert("key2", "value2")
        self.datastore.insert("key3", "value3")
        self.datastore.insert("another_key", "value4")

        pattern = r"^key\d+$"
        keys = self.datastore.keys(pattern)
        self.assertEqual(set(keys), {"key1", "key2", "key3"})

        pattern = r".*_key$"
        keys = self.datastore.keys(pattern)
        self.assertEqual(set(keys), {"another_key"})
