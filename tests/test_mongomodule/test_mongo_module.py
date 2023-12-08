import unittest
import unittest.mock
# from src.database.mongo_module import MongoModule
import sys
sys.path.append('/home/gustavo/ES/Engenharia_Software/')

from src.database.mongo_module import MongoModule


class TestMongoModule(unittest.TestCase):

    def setUp(self):
        self.mongo_module = MongoModule(host="localhost", collection_name="test_collection")

    def test_connect(self):
        with unittest.mock.patch('pymongo.MongoClient') as mock_mongo:
            self.mongo_module.connect()
            mock_mongo.assert_called_once_with(host="localhost")

    def test_disconnect(self):
        pass

    def test_insert_data(self):
        pass

    def test_delete_data(self):
        pass

    def test_update_data(self):
        pass

    def test_select_data(self):
        pass

if __name__ == '__main__':
    unittest.main()
