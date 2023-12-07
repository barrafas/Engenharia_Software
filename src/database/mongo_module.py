from pymongo import MongoClient
from .database_module import DatabaseModule

class MongoModule(DatabaseModule):
    def __init__(self, host, collection_name):
        ...

    def connect(self):
        ...

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


