import unittest
from src.user.user_management import UserManagement, \
UsernameCantBeBlank, User
from unittest.mock import Mock, MagicMock, patch
from src.database.mongo_module import MongoModule, DuplicatedIDError, NonExistentIDError
import bcrypt

class TestUserManagementModule(unittest.TestCase):
    def setUp(self):
        # Set up for the tests
        UserManagement._instance = None
        # Cria um mock para a interface DatabaseModule
        self.db = Mock()
        self.user_management = UserManagement.get_instance(self.db)

    def test_create_user_success(self):
        # Test creating a new user successfully
        self.db.insert_data = MagicMock(return_value = 
                                    [{"username": "test_user", 
                                      "email": "test_email", 
                                      "hashed_password": "test_hashed_password"}])
        
        self.db.select_data = MagicMock(return_value = [])
        
        result = self.user_management.create_user(username="test_user", 
                        email="test_email", password="test_password", id="1")
        self.assertEqual(result.username, "test_user")
        self.assertEqual(result.email, "test_email")
        self.assertTrue(bcrypt.checkpw("test_password".encode('utf-8'), 
                                       result.hashed_password.encode('utf-8')), 
                        result.hashed_password)

    def test_create_existing_user(self):
        # Test creating a user that already exists
        self.db.select_data = MagicMock(return_value = 
                                    [{"username": "test_user", 
                                      "email": "test_email", 
                                      "hashed_password": "test_hashed_password"}])
        
        with self.assertRaises(DuplicatedIDError) as context:
            self.user_management.create_user(username="test_user", 
                            email="test_email", password="test_password", id="1")
        self.assertEqual(str(context.exception),
                            "Usuário test_user já existe")
        
    def test_create_blank_username(self):
        # Test creating a user with a blank username
        with self.assertRaises(UsernameCantBeBlank) as context:
            self.user_management.create_user(username="", 
                            email="test_email", password="test_password", id="1")
        self.assertEqual(str(context.exception),
                            "Nome de usuário não pode ser vazio")

    def test_hash_password(self):
        # Test hashing a password
        password = "test_password"
        hashed_password = self.user_management.hash_password(password)
        self.assertTrue(bcrypt.checkpw(password.encode('utf-8'), hashed_password))

    def test_delete_user(self):
        # Test deleting a user
        self.db.select_data = MagicMock(return_value = ['a'])


        self.db.delete_data = MagicMock()
        self.user_management.delete_user("test_user")
        self.db.delete_data.assert_called_once_with("users", {"_id": "test_user"})

    def test_delete_nonexistent_user(self):
        # Test deleting a nonexistent user
        self.db.select_data = MagicMock(return_value = [])
        with self.assertRaises(NonExistentIDError) as context:
            self.user_management.delete_user("id2")
        self.assertEqual(str(context.exception),
                            "Usuário id2 não existe")

    def test_user_exists(self):
        # Test checking if a user exists
        self.db.select_data = MagicMock(return_value = ['a'])
        result = self.user_management.user_exists("test_user")
        self.assertTrue(result)

    def test_user_doesnt_exist(self):
        # Test checking if a user doesnt exists
        self.db.select_data = MagicMock(return_value = [])
        result = self.user_management.user_exists("test_user")
        self.assertFalse(result)

    def test_update_user(self):
        # Test updating a user
        self.db.select_data = MagicMock(return_value = ['a'])
        self.db.update_data = MagicMock()
        self.user_management.users = {"test_user": User("test_user", "test_email",
                                                        "test_password", "test_id")}
        self.user_management.update_user("test_user")
        self.db.update_data.assert_called_once_with("users", {"_id": "test_user"},
                                {'id': 'test_user', 'username': 'test_email', 
                                'email': 'test_password', 'schedules': 'test_id', 
                                'password': None, 'user_preferences': {}})
        
    def test_update_nonexistent_user(self):
        # Test updating a nonexistent user
        self.db.select_data = MagicMock(return_value = [])
        with self.assertRaises(NonExistentIDError) as context:
            self.user_management.update_user("id2")
        self.assertEqual(str(context.exception),
                            "Usuário id2 não existe")
        
    def test_add_schedule_to_user(self):
        # Test adding a schedule to a user
        self.db.select_data = MagicMock(return_value = ['a'])
        self.db.update_data = MagicMock()
        self.user_management.users = {"test_id": User("test_id", "test_user",
                                                        "test_email", [],
                                                        "test_password")}
        self.user_management.add_schedule_to_user("test_id", "test_schedule")
        self.db.update_data.assert_called_once_with("users", {"_id": "test_id"},
                                {'id': 'test_id', 'username': 'test_user', 
                                'email': 'test_email', 'schedules': ["test_schedule"], 
                                'password': "test_password", 'user_preferences': {}})
        
    def test_add_schedule_to_nonexistant_user(self):
        # Test adding a schedule to a nonexistent user
        self.db.select_data = MagicMock(return_value = [])
        with self.assertRaises(NonExistentIDError) as context:
            self.user_management.add_schedule_to_user("id2", "test_schedule")
        self.assertEqual(str(context.exception),
                            "Usuário id2 não existe")

        
if __name__ == '__main__':
    unittest.main()
