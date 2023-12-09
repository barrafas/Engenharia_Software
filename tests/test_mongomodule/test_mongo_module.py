import unittest
import unittest.mock
import logging
import sys
sys.path.append('/home/gustavo/ES/Engenharia_Software/')
from src.database.mongo_module import MongoModule

class TestMongoModule(unittest.TestCase):

    def setUp(self):
        self.HOST = "localhost"
        self.mongo_module = MongoModule(host=self.HOST, port=27018, database_name='test')

    def tearDown(self):
        if self.mongo_module._client:
            self.mongo_module._db['teste'].delete_many({})
            self.mongo_module.disconnect()

    def test_connect(self):
        self._connect_to_database()
        self._assert_connection()
        self._assert_error_if_already_connected()

    def test_disconnect(self):
        self._connect_to_database()
        self._disconnect_from_database()
        self._assert_disconnected()
        self._assert_error_if_already_disconnected()

    def test_insert_data(self):
        self._connect_and_insert_data()
        self._disconnect_and_insert_data()

    def test_delete_data(self):
        self._connect_and_delete_data()
        self._disconnect_and_delete_data()

    def test_update_data(self):
        self._connect_insert_and_update_data()
        self._disconnect_and_update_data()

    def test_select_data(self):
        self._connect_to_database()
        expected_result = [{"_id": unittest.mock.ANY, "test": "test3"}]
        self._connect_insert_and_select_data_internal(query={"test": "test3"}, expected_result=expected_result)
        expected_result2 = [{"_id": unittest.mock.ANY, "test": "test4"}]
        self._connect_insert_and_select_data_internal(query={"test": "test4"}, expected_result=expected_result2)
        expected_result3 = [{"_id": unittest.mock.ANY, "test": "test5"}]
        self._connect_insert_and_select_data_internal(query={"test": "test5"}, expected_result=expected_result3)


    def _connect_to_database(self):
        with unittest.mock.patch('pymongo.MongoClient') as mock_mongo:
            self.mongo_module.connect()
            mock_mongo.assert_called_once_with(host=self.HOST, port=27018, username=None, password=None)
            mock_mongo.assert_called_with(host=self.HOST, port=27018, username=None, password=None)
            mock_mongo.assert_called_once()
            self.assertIsNotNone(self.mongo_module._client)
            self.assertIsNotNone(self.mongo_module._db)

    def _assert_connection(self):
        with self.assertRaises(Exception):
            self.mongo_module.connect()

    def _assert_error_if_already_connected(self):
        with self.assertRaises(Exception):
            self.mongo_module.connect()

    def _disconnect_from_database(self):
        self.mongo_module.disconnect()
        self.assertIsNone(self.mongo_module._client)
        self.assertIsNone(self.mongo_module._db)

    def _assert_disconnected(self):
        with self.assertRaises(Exception):
            self.mongo_module.disconnect()

    def _assert_error_if_already_disconnected(self):
        with self.assertRaises(Exception):
            self.mongo_module.disconnect()

    def _connect_and_insert_data(self):
        self._connect_to_database()
        with unittest.mock.patch.object(self.mongo_module._db['teste'], 'insert_one') as mock_insert:
            self.mongo_module.insert_data(collection_name='teste',
                                          data={"test": "test"})
            mock_insert.assert_called_once_with({"test": "test"})

    def _disconnect_and_insert_data(self):
        self._disconnect_from_database()
        with self.assertRaises(Exception):
            self.mongo_module.insert_data(collection_name='teste',
                                          data={"test": "test"})

    def _connect_and_delete_data(self):
        self._connect_to_database()
        with unittest.mock.patch.object(self.mongo_module._db['teste'], 'delete_one') as mock_delete:
            self.mongo_module.delete_data(collection_name='teste',
                                          condition={"test": "test"})
            mock_delete.assert_called_once_with({"test": "test"})

    def _disconnect_and_delete_data(self):
        self._disconnect_from_database()
        with self.assertRaises(Exception):
            self.mongo_module.delete_data({"test": "test"})

    def _connect_insert_and_update_data(self):
        self._connect_to_database()
        self._connect_insert_and_update_data_internal()

    def _disconnect_and_update_data(self):
        self._disconnect_from_database()
        with self.assertRaises(Exception):
            self.mongo_module.update_data(collection_name='teste',
                                          condition={"test": "test"}, 
                                          new_data={"test": "test"})

    def _connect_insert_and_update_data_internal(self):
        self.mongo_module.insert_data(collection_name='teste',
                                      data={"test": "test"})

        with unittest.mock.patch.object(self.mongo_module._db['teste'], 'update_one') as mock_update:
            self.mongo_module.update_data(collection_name='teste',
                                          condition={"test": "test"}, 
                                          new_data={"test": "test2"})
            
            mock_update.assert_called_once_with({"test": "test"}, {"test": "test2"})

    def _connect_insert_and_select_data_internal(self, query, expected_result):
        self.mongo_module.insert_data(collection_name='teste',
                                      data={"test": "test3"})

        
        
        with unittest.mock.patch.object(self.mongo_module._db['teste'], 'find') as mock_find:
            mock_find.return_value = expected_result
            result = self.mongo_module.select_data(collection_name='teste', 
                                                   condition=query)

        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("TestMongoModule.test_select_data").setLevel(logging.DEBUG)
    unittest.main()
