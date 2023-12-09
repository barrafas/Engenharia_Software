from abc import ABC, abstractmethod

class DatabaseModule(ABC):
    @abstractmethod
    def connect(self, host, db_name):
        """Connect to the database."""

    @abstractmethod
    def disconnect(self):
        """Disconnect from the database."""

    @abstractmethod
    def insert_data(self, collection_name, data):
        """Execute a database query."""

    @abstractmethod
    def delete_data(self, collection_name, data):
        """Delete data from the database."""

    @abstractmethod
    def update_data(self, collection_name, condition, data):
        """Update data in the database."""

    @abstractmethod
    def select_data(self, collection_name, condition):
        """Fetch data from the database."""
