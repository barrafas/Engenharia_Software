import pymongo
from src.database.database_module import DatabaseModule

class MongoModule(DatabaseModule):
    """
    This class implements the DatabaseModule interface for MongoDB.

    Attributes:
        host (str): The host address of the database.
        port (int): The port of the database.
        user (str): The user of the database.
        password (str): The password of the database.
        database_name (str): The name of the database.
        collection_name (str): The name of the collection.
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
    def __init__(self, 
                 host: str, 
                 port: int, 
                 database_name: str,
                 collection_name: str,
                 user: str = None,
                 password: str = None,):
        """
        Constructor method.

        Args:
            host (str): The host address of the database.
            port (int): The port of the database.
            database_name (str): The name of the database.
            collection_name (str): The name of the collection.
            user (str): The user of the database.
            password (str): The password of the database.
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database_name = database_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        """
        Connect to the database.
        Raises:
            Exception: If already connected to the database.
        """
        if self.client:
            raise Exception("Already connected to the database.")
        
        self.client = pymongo.MongoClient(host=self.host, port=self.port, username=self.user, password=self.password)
        self.db = self.client[self.database_name]
        self.collection = self.db[self.collection_name]
        
    def disconnect(self):
        """
        Disconnect from the database.
        Raises:
            Exception: If not connected to the database.
        """
        if not self.client:
            raise Exception("Not connected to the database.")
        self.client = None
        self.db = None
        self.collection = None

    def insert_data(self, data):
        """
        Execute a database query.
        
        Args:
            query (str): The query to execute.
            
        Raises:
            Exception: If not connected to the database.
        """
        if not self.client:
            raise Exception("Not connected to the database.")
        self.collection.insert_one(data)

    def delete_data(self, data):
        """
        Delete data from the database.

        Args:
            data (dict): The data to delete.

        Raises:
            Exception: If not connected to the database.
        """
        self.collection.delete_one(data)

    def update_data(self, where, data):
        """
        Update data in the database.

        Args:
            where (dict): The data to update.
            data (dict): The data to update to.

        Raises:
            Exception: If not connected to the database.
        """
        self.collection.update_one(where, data)

    def select_data(self, query=None):
        """
        Fetch data from the database.

        Args:
            query (dict): The query to execute.

        Returns:
            list: The result of the query.
        """
        result = list(self.collection.find(query))

        return result
