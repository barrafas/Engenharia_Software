import pymongo
from src.database.database_module import DatabaseModule

class MongoModule(DatabaseModule):
    def __init__(self, 
                 host: str, 
                 port: int, 
                 database_name: str,
                 collection_name: str,
                 user: str = None,
                 password: str = None,):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database_name = database_name
        self.collection_name = collection_name
        self.client = None
        self.db = None

    def connect(self):
        if self.client:
            raise Exception("Already connected to the database.")
        
        self.client = pymongo.MongoClient(host=self.host, port=self.port, username=self.user, password=self.password)
        self.db = self.client[self.database_name]
        self.collection = self.db[self.collection_name]
        
    def disconnect(self):
        if not self.client:
            raise Exception("Not connected to the database.")
        self.client = None
        self.db = None
        self.collection = None

    def insert_data(self, query):
        ...

    def delete_data(self, query):
        ...

    def update_data(self, query):
        ...

    def select_data(self, query):
        ...


