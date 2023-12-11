""" Interface for database modules.

Classes:
    DatabaseModule

Abstract Methods:
    connect
    disconnect
    insert_data
    delete_data
    update_data
    select_data
"""

from abc import ABC, abstractmethod

class DatabaseModule(ABC):
    """
    Interface for database modules.

    Methods:
        connect
        disconnect
        insert_data
        delete_data
        update_data
        select_data

    Attributes:
        host (str): database host
        port (int): database port
        database_name (str): database name
        user (str): database user
        password (str): database password
    """
    @abstractmethod
    def connect(self):
        """Connect to the database."""

    @abstractmethod
    def disconnect(self):
        """Disconnect from the database."""

    @abstractmethod
    def insert_data(self, collection_name, data):
        """Execute a database query."""

    @abstractmethod
    def delete_data(self, collection_name, condition):
        """Delete data from the database."""

    @abstractmethod
    def update_data(self, collection_name, condition, new_data):
        """Update data in the database."""

    @abstractmethod
    def select_data(self, collection_name, condition):
        """Fetch data from the database."""
