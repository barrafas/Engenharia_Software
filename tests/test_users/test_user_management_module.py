"""
Test for user_management.py
"""

import unittest
from src.user.user_management import UserManagement, \
UsernameCantBeBlank, User
from unittest.mock import Mock, MagicMock, patch
from src.database.mongo_module import MongoModule, DuplicatedIDError, NonExistentIDError
from src.calendar_elements.element_management import ElementManagement
from src.calendar_elements.element_interface import Element
from src.schedule.schedule_management import ScheduleManagement
import bcrypt

class TestUserManagementModule(unittest.TestCase):
    def setUp(self):
        """Set up for the tests"""
        UserManagement._instance = None
        # Cria um mock para a interface DatabaseModule
        self.db_module = Mock()
        self.user_management = UserManagement.get_instance(self.db_module)

        ElementManagement._instance = None
        self.db_module = MagicMock()
        self.element_management = ElementManagement.get_instance(
            self.db_module)

        ScheduleManagement._instance = None
        self.schedule_management = ScheduleManagement.get_instance(
            self.db_module)

    def test_create_user_success(self):
        """Test creating a new user successfully"""
        self.db_module.insert_data = MagicMock(return_value =
                                    [{"username": "test_user",
                                      "email": "test_email", 
                                      "hashed_password": "test_hashed_password"}])
        self.db_module.select_data = MagicMock(return_value = [])
        result = self.user_management.create_user(username="test_user",
                        email="test_email", password="test_password", user_id="1")
        self.assertEqual(result.username, "test_user")
        self.assertEqual(result.email, "test_email")
        self.assertTrue(bcrypt.checkpw("test_password".encode('utf-8'),
                                       result.hashed_password.encode('utf-8')),
                        result.hashed_password)

        # def mock_select_data(collection, query):
        #     if collection == "users" and query == {"_id": "test_user1"}:
        #         return [{"_id": "test_user1",
        #                 "username": "test_user",
        #                 "email": "test_email", 
        #                 "hashed_password": "test_hashed_password"}]
        
        # self.user_management.db_module.select_data = MagicMock(side_effect=mock_select_data)
        # self.user_management.db_module.insert_data = MagicMock()
        # user_id = "test_user1"
        # username = "test_user"
        # email = "test_email"
        # password = "test_password"
        # user_preferences = {}
        # user = User(user_id, username, email, [], password, user_preferences)
        # self.user_management.user_exists = MagicMock(return_value=False)
        # self.user_management.create_user(username, email, password, user_preferences, user_id)
        
        # self.user_management.db_module.insert_data.assert_called_once_with("users", {"_id": user_id,



    def test_create_existing_user(self):
        """Test creating a user that already exists"""
        self.db_module.select_data = MagicMock(return_value =
                                    [{"username": "test_user",
                                      "email": "test_email", 
                                      "hashed_password": "test_hashed_password"}])

        with self.assertRaises(DuplicatedIDError) as context:
            self.user_management.create_user(username="test_user",
                            email="test_email", password="test_password", id="1")
        self.assertEqual(str(context.exception),
                            "Usuário test_user já existe")

    def test_create_blank_username(self):
        """Test creating a user with a blank username"""
        with self.assertRaises(UsernameCantBeBlank) as context:
            self.user_management.create_user(username="",
                            email="test_email", password="test_password", id="1")
        self.assertEqual(str(context.exception),
                            "Nome de usuário não pode ser vazio")

    def test_hash_password(self):
        """Test hashing a password"""
        password = "test_password"
        hashed_password = self.user_management.hash_password(password)
        self.assertTrue(bcrypt.checkpw(password.encode('utf-8'), hashed_password))

    def test_delete_user(self):
        """Test deleting a user"""
        self.db_module.select_data = MagicMock(return_value = ['a'])
        self.db_module.delete_data = MagicMock()
        self.user_management.delete_user("test_user")
        self.db_module.delete_data.assert_called_once_with("users", {"_id": "test_user"})

    def test_delete_nonexistent_user(self):
        """Test deleting a nonexistent user"""
        self.db_module.select_data = MagicMock(return_value = [])
        with self.assertRaises(NonExistentIDError):
            self.user_management.delete_user("id2")

    def test_user_exists_returns_true(self):
        """Test that user_exists returns True when a user with the given id exists"""
        # Arrange
        user_id = 'existing_user_id'
        mock_db_module = MagicMock()
        mock_db_module.select_data.return_value = [{'_id': user_id, 
            'username': 'username', 'email': 'email', 'schedules': []}]
        user_management = UserManagement(mock_db_module)

        # Act
        result = user_management.user_exists(user_id)

        # Assert
        self.assertTrue(result)

    def test_user_exists_returns_false(self):
        """Test that user_exists returns False when a user with the given id does not exist"""
        # Arrange
        user_id = 'non_existent_user_id'
        mock_db_module = MagicMock()
        mock_db_module.select_data.return_value = []
        user_management = UserManagement(mock_db_module)

        # Act
        result = user_management.user_exists(user_id)

        # Assert
        self.assertFalse(result)

    def test_update_user(self):
        """Test that update_user calls update_data with the correct arguments"""
        # Arrange
        user_id = 'existing_user_id'
        user_info = {'_id': user_id, 'username': 'username',
                 'email': 'email', 'schedules': [],
                 'hashed_password': None, 'user_preferences': {}}
        user = User(**user_info)
        mock_db_module = MagicMock()
        mock_db_module.select_data.return_value = [user_info]
        user_management = UserManagement(mock_db_module)
        user_management.users[user_id] = user

        # Act
        user_management.update_user(user_id)

        # Assert
        mock_db_module.update_data.assert_called_once_with('users', {"_id": user_id}, user_info)


    def test_update_nonexistent_user(self):
        """Test that update_user raises NonExistentIDError when the user does not exist"""
        # Arrange
        user_id = 'non_existent_user_id'
        mock_db_module = MagicMock()
        mock_db_module.select_data.return_value = []
        user_management = UserManagement(mock_db_module)

        # Act and Assert
        with self.assertRaises(NonExistentIDError):
            user_management.update_user(user_id)

    def test_add_schedule_to_user(self):
        """Test adding a schedule to a user"""
        self.db_module.select_data = MagicMock(return_value = ['a'])
        self.db_module.update_data = MagicMock()
        self.user_management.user_exists = MagicMock(return_value=True)
        self.user_management.users = {"test_id": User("test_id", "test_user",
                                                        "test_email", [],
                                                        "test_password")}
        self.user_management.add_schedule_to_user("test_id", "test_schedule",
                                                  "write")
        self.db_module.update_data.assert_called_once_with("users", {"_id": "test_id"},
                                {'id': 'test_id', 'username': 'test_user',
                                'email': 'test_email', 'schedules': ["test_schedule"], 
                                'password': "test_password", 'user_preferences': {}})

    def test_add_schedule_to_nonexistant_user(self):
        """Test adding a schedule to a nonexistent user"""
        self.db_module.select_data = MagicMock(return_value = [])
        self.user_management.user_exists = MagicMock(return_value=False)
        with self.assertRaises(NonExistentIDError):
            self.user_management.add_schedule_to_user("id2", "test_schedule",
            "write")


if __name__ == '__main__':
    unittest.main()
