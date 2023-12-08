import pymongo
from src.database.database_module import DatabaseModule

class MongoModule(DatabaseModule):
    def __init__(self, host, collection_name):
        self.host = host
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        self.client = pymongo.MongoClient(host=self.host)

    def disconnect(self):
        ...

    def insert_data(self, query):
        ...

    def delete_data(self, query):
        ...

    def update_data(self, query):
        ...

    def select_data(self, query):
        ...


