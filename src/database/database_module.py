from abc import ABC, abstractmethod

class DatabaseModule(ABC):
    @abstractmethod
    def connect(self):
        """Connect to the database."""

    @abstractmethod
    def disconnect(self):
        """Disconnect from the database."""

    @abstractmethod
    def execute_query(self, query):
        """Execute a database query."""

    @abstractmethod
    def fetch_data(self, query):
        """Fetch data from the database."""
