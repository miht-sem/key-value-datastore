# Simple In-Memory Datastore

A lightweight in-memory datastore, providing basic key-value storage operations with transaction support.

## Features

- Key-value storage
- Transaction support with commit and rollback
- Regular expression pattern-based key queries
- Unittests for core functionalities
- Docker and docker-compose integration
- GitHub CI/CD pipeline

## Getting Started

### Prerequisites

- Python 3.x
- Docker (optional)

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/simple-in-memory-datastore.git
```

(Optional) Build the Docker image:

```bash
docker-compose build
```

## Running the Tests

Run the tests using Python:

```bash
python -m unittest discover tests
```

Alternatively, run the tests using Docker:

```bash
docker-compose run --rm app python -m unittest discover tests
```

## Usage

Import the Datastore class:

```python
from src.datastore.datastore import Datastore
```

Create a new datastore instance:

```python
datastore = Datastore(in_memory=True)
```

### Perform basic operations:

- Insert a key-value pair
```python 
datastore.insert("key1", "value1") 
```

- Update a key-value pair
```python 
datastore.update("key1", "value2")
```

- Select a value by key
```python 
datastore.select("key1")
```

- Delete a key-value pair
```python 
datastore.delete("key1")
```

### Perform operations in a transaction:

- Begin a transaction
```python 
datastore.begin()
```

- Insert a key-value pair in the transaction
```python 
datastore.insert("key2", "value1")
```

- Update a key-value pair in the transaction
```python 
datastore.update("key2", "value2")
```

- Commit the transaction
```python 
datastore.commit()
```

### Query keys using regular expression patterns:

- Insert some key-value pairs
```python 
datastore.insert("key1", "value1")
datastore.insert("key2", "value2")
datastore.insert("key3", "value3")
datastore.insert("another_key", "value4")
```

- Query keys using a pattern
```python
pattern = r"^key\d+$"
matching_keys = datastore.keys(pattern)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
