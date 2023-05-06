from core.datastore import Datastore
from core.enums import DatastoreStatus


def test_datastore_transactions():
    datastore = Datastore(in_memory=True)

    # Inserting a new key-value pair
    assert datastore.insert("key1", "value1").status == DatastoreStatus.OK

    # Trying to insert a duplicate key
    assert datastore.insert("key1", "value2").status == DatastoreStatus.KEY_ALREADY_EXISTS

    # Updating an existing key
    assert datastore.update("key1", "value2").status == DatastoreStatus.OK

    # Selecting a value by key
    assert datastore.select("key1").value == "value2"

    # Deleting a key-value pair
    assert datastore.delete("key1").status == DatastoreStatus.OK

    # Selecting a non-existent key
    assert datastore.select("nonexistent_key").status == DatastoreStatus.KEY_NOT_FOUND

    # Insert some key-value pairs
    datastore.insert("key1", "value1")
    datastore.insert("key2", "value2")
    datastore.insert("key3", "value3")
    datastore.insert("another_key", "value4")

    # Query keys using regular expression patterns
    pattern = r"^key\d+$"
    assert set(datastore.keys(pattern)) == {"key1", "key2", "key3"}

    pattern = r".*_key$"
    assert set(datastore.keys(pattern)) == {"another_key"}

    # Beginning a transaction
    assert datastore.begin().status == DatastoreStatus.OK

    # Performing multiple operations in a transaction and committing
    assert datastore.insert("key4", "value1").status == DatastoreStatus.IN_TRANSACTION_LIST
    assert datastore.update("key4", "value2").status == DatastoreStatus.IN_TRANSACTION_LIST
    assert datastore.commit().status == DatastoreStatus.OK

    # Selecting a value modified in the transaction
    assert datastore.select("key4").value == "value2"

    # Starting another transaction
    assert datastore.begin().status == DatastoreStatus.OK

    # Performing multiple operations and rolling back
    assert datastore.insert("key5", "value1").status == DatastoreStatus.IN_TRANSACTION_LIST
    assert datastore.update("nonexistent_key", "value").status == DatastoreStatus.IN_TRANSACTION_LIST
    assert datastore.rollback().status == DatastoreStatus.OK

    # Verifying that the changes from the rolled back transaction are not present
    assert datastore.select("key5").status == DatastoreStatus.KEY_NOT_FOUND


def print_datastore_test():
    datastore = Datastore(in_memory=True)

    # Inserting a new key-value pair
    print("Inserting (key1, value1):", datastore.insert("key1", "value1"))

    # Trying to insert a duplicate key
    print("Inserting (key1, value2):", datastore.insert("key1", "value2"))

    # Updating an existing key
    print("Updating (key1, value2):", datastore.update("key1", "value2"))

    # Selecting a value by key
    print("Selecting key1:", datastore.select("key1"))

    # Deleting a key-value pair
    print("Deleting key1:", datastore.delete("key1"))
    print("Deleting key1:", datastore.delete("key1"))

    # Selecting a non-existent key
    print("Selecting nonexistent_key:", datastore.select("nonexistent_key"))

    # Beginning a transaction
    print("Starting a transaction:", datastore.begin())

    # Performing multiple operations in a transaction and committing
    print("Inserting (key2, value1) in transaction:", datastore.insert("key2", "value1"))
    print("Updating (key2, value2) in transaction:", datastore.update("key2", "value2"))
    print("Committing transaction:", datastore.commit())

    # Selecting a value modified in the transaction
    print("Selecting key2:", datastore.select("key2"))

    # Starting another transaction
    print("Starting a transaction:", datastore.begin())

    # Performing multiple operations and rolling back
    print("Inserting (key3, value1) in transaction:", datastore.insert("key3", "value1"))
    print("Updating (nonexistent_key, value) in transaction:", datastore.update("nonexistent_key", "value"))
    print("Committing transaction:", datastore.commit())

    # Verifying that the changes from the rolled back transaction are not present
    print("Selecting key3:", datastore.select("key3"))

    # Insert some key-value pairs
    datastore.insert("key1", "value1")
    datastore.insert("key2", "value2")
    datastore.insert("key3", "value3")
    datastore.insert("another_key", "value4")

    # Query keys using regular expression patterns
    pattern = r"^key\d+$"
    print(f"Keys matching pattern '{pattern}':", datastore.keys(pattern))

    pattern = r".*_key$"
    print(f"Keys matching pattern '{pattern}':", datastore.keys(pattern))


def main():
    test_datastore_transactions()
    print_datastore_test()


if __name__ == "__main__":
    main()
