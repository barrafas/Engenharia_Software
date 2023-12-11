""" mongo_module.py

This module defines a MongoDB implementation of the DatabaseModule interface 
and demonstrates the Singleton pattern.

Classes:
    - MongoModule(DatabaseModule): Implements the DatabaseModule interface for 
    MongoDB.
        Attributes:
            - host (str): The host address of the database.
            - port (int): The port of the database.
            - user (str): The user of the database.
            - password (str): The password of the database.
            - database_name (str): The name of the database.
            - client (MongoClient): The MongoClient object.
            - db (Database): The Database object.

        Methods:
            - connect(): Connects to the database.
            - disconnect(): Disconnects from the database.
            - insert_data(collection_name, data): Inserts data into the 
            database.
            - delete_data(collection_name, condition): Deletes data from the 
            database.
            - update_data(collection_name, condition, new_data): Updates data 
            in the database.
            - select_data(collection_name, condition): Selects data from the 
            database.

    Note: The MongoModule class follows the Singleton pattern to ensure a 
    single instance throughout the program.

Usage:
    The module can be used to interact with a MongoDB database by creating an 
    instance of the MongoModule class. The Singleton pattern ensures that 
    multiple instances of the class refer to the same database connection.
"""
import pymongo

from src.database.database_module import DatabaseModule
from src.database.utils import TimeoutDecorator

class DuplicatedIDError(Exception):
    """Raised when the ID already exists"""

class NonExistentIDError(Exception):
    """Raised when the ID does not exist"""

class ConnectionDBError(Exception):
    """Raised when the connection to the database fails"""

class MongoModule(DatabaseModule):
    """
    This class implements the DatabaseModule interface for MongoDB.

    Attributes:
        host (str): The host address of the database.
        port (int): The port of the database.
        user (str): The user of the database.
        password (str): The password of the database.
        database_name (str): The name of the database.
        client (MongoClient): The MongoClient object.
        db (Database): The Database object.

    Methods:
        connect: Connects to the database.
        disconnect: Disconnects from the database.
        insert_data: Inserts data into the database.
        delete_data: Deletes data from the database.
        update_data: Updates data in the database.
        select_data: Selects data from the database.
    """

    _instance = None

    def __init__(
        self,
        host: str,
        port: int,
        database_name: str,
        user: str = None,
        password: str = None,
    ):
        """
        Constructor method.

        Args:
            _host (str): The host address of the database.
            _port (int): The port of the database.
            _database_name (str): The name of the database.
            _user (str): The user of the database.
            _password (str): The password of the database.
            _client (MongoClient): The MongoClient object.
            _db (Database): The Database object.
            _collection (Collection): The Collection object.

        """
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._database_name = database_name
        self._client = None
        self._db = None
        self.collection = None

    def __new__(cls, *args, **kwargs):
        """
        Singleton constructor method.

        Returns:
            MongoModule: The MongoModule instance.
        """
        if not cls._instance:
            cls._instance = super(MongoModule, cls).__new__(cls)
        return cls._instance

    def connect(self):
        """
        Connect to the database.
        Raises:
            Exception: If already connected to the database.
        """
        # time.sleep(10) # Here just to test the timeout decorator

        if self._client:
            raise ConnectionDBError("Already connected to the database.")

        self._client = pymongo.MongoClient(
            host=self._host,
            port=self._port,
            username=self._user,
            password=self._password,
        )
        self._db = self._client[self._database_name]

    def disconnect(self):
        """
        Disconnect from the database.
        Raises:
            Exception: If not connected to the database.
        """
        if not self._client:
            raise ConnectionDBError("Not connected to the database.")
        # disconnect from the database
        self._client.close()

        self._client = None
        self._db = None

    def insert_data(self,
                    collection_name: str,
                    data: dict):
        """
        Execute a database query.

        Args:
            collection_name (str): The name of the collection.
            data (dict): The data to insert.

        Raises:
            Exception: If not connected to the database.
        """
        if not self._client:
            raise ConnectionError("Not connected to the database.")
        self._db[collection_name].insert_one(data)

    def delete_data(self,
                    collection_name: str,
                    condition: dict):
        """
        Delete data from the database.

        Args:
            collection_name (str): The name of the collection.
            condition (dict): The condition to match.

        Raises:
            Exception: If not connected to the database.
        """
        self._db[collection_name].delete_one(condition)

    def update_data(self,
                    collection_name: str,
                    condition: dict,
                    new_data: dict):
        """
        Update data in the database.

        Args:
            collection_name (str): The name of the collection.
            condition (dict): The condition to match.
            new_data (dict): The new data to insert.

        Raises:
            Exception: If not connected to the database.
        """
        new_data = {"$set": new_data}
        self._db[collection_name].update_one(condition, new_data)

    def select_data(self,
                    collection_name,
                    condition):
        """
        Fetch data from the database.

        Args:
            collection_name (str): The name of the collection.
            condition (dict): The condition to match.

        Returns:
            list: The result of the query.
        """
        result = list(self._db[collection_name].find(condition))

        return result

if __name__ == "__main__": # pragma: no cover
    mongo_module = MongoModule(  # pragma: no cover
        host="localhost", port=27017, database_name="test")  # pragma: no cover
     # pragma: no cover
    mongo_module2 = MongoModule(  # pragma: no cover
        host="localhost", port=27017, database_name="test")  # pragma: no cover
    # pragma: no cover
    if mongo_module == mongo_module2:  # pragma: no cover
        print("Singleton works, both variables contain the same instance.")  # pragma: no cover
    else:  # pragma: no cover
        print("Singleton failed, variables contain different instances.")  # pragma: no cover
    # pragma: no cover
    # timeout decorator  # pragma: no cover
    mongo_module = TimeoutDecorator(mongo_module, timeout_seconds=5)  # pragma: no cover
    mongo_module.connect()  # pragma: no cover
