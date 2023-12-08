import unittest
import unittest.mock
# from src.database.mongo_module import MongoModule
import sys
sys.path.append('/home/gustavo/ES/Engenharia_Software/')

from src.database.mongo_module import MongoModule


class TestMongoModule(unittest.TestCase):

    def setUp(self):
        self.HOST = "localhost"
        self.mongo_module = MongoModule(host=self.HOST, collection_name="test_collection", database_name="test_db", port=27017)

    def test_connect(self):
        with unittest.mock.patch('pymongo.MongoClient') as mock_mongo:
            self.mongo_module.connect()
            mock_mongo.assert_called_once_with(host=self.HOST, port=27017, username=None, password=None)
            mock_mongo.assert_called_with(host=self.HOST, port=27017, username=None, password=None)
            mock_mongo.assert_called_once()
            self.assertIsNotNone(self.mongo_module.client)
            self.assertIsNotNone(self.mongo_module.db)
            self.assertIsNotNone(self.mongo_module.collection)

            # assert error
            with self.assertRaises(Exception):
                self.mongo_module.connect()

    def test_disconnect(self):
        self.mongo_module.connect()
        self.mongo_module.disconnect()
        self.assertIsNone(self.mongo_module.client)
        self.assertIsNone(self.mongo_module.db)
        self.assertIsNone(self.mongo_module.collection)

        with self.assertRaises(Exception):
            self.mongo_module.disconnect()

    def test_insert_data(self):
        self.mongo_module.connect()

        with unittest.mock.patch.object(self.mongo_module.collection, 'insert_one') as mock_insert:
            self.mongo_module.insert_data({"test": "test"})
            mock_insert.assert_called_once_with({"test": "test"})

        self.mongo_module.disconnect()
        with self.assertRaises(Exception):
            self.mongo_module.insert_data({"test": "test"})


    def test_delete_data(self):
        self.mongo_module.connect()

        with unittest.mock.patch.object(self.mongo_module.collection, 'delete_one') as mock_delete:
            self.mongo_module.delete_data({"test": "test"})
            mock_delete.assert_called_once_with({"test": "test"})

        self.mongo_module.disconnect()
        with self.assertRaises(Exception):
            self.mongo_module.delete_data({"test": "test"})

    def test_update_data(self):
        pass

    def test_select_data(self):
        pass

if __name__ == '__main__':
    unittest.main()
