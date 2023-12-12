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
from src.schedule.schedule_model import Schedule
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
        """Test that create_user calls insert_data with the correct arguments"""
        # Arrange
        username = 'username'
        email = 'email@example.com'
        password = 'password'
        user_preferences = {'preference': 'value'}
        user_id = 'new_user_id'
        hashed_password = 'hashed_password'
        mock_db_module = MagicMock()
        mock_db_module.select_data.return_value = []
        user_management = UserManagement(mock_db_module)
        user_management.hash_password = MagicMock(return_value=hashed_password.encode('utf-8'))
        expected_user_info = {"_id": user_id,
                            "username": username,
                            "email": email,
                            "schedules": [],
                            "hashed_password": hashed_password,
                            "user_preferences": user_preferences}
        # Act
        user_management.create_user(username, email, password, user_preferences, user_id)
        # Assert
        mock_db_module.insert_data.assert_called_once_with('users', expected_user_info)

    def test_create_existing_user(self):
        """Test that create_user raises DuplicatedIDError when the user id already exists"""
        # Arrange
        username = 'username'
        email = 'email@example.com'
        password = 'password'
        user_preferences = {'preference': 'value'}
        user_id = 'existing_user_id'
        mock_db_module = MagicMock()
        mock_db_module.select_data.return_value = [{'_id': user_id}]
        user_management = UserManagement(mock_db_module)

        # Act and Assert
        with self.assertRaises(DuplicatedIDError):
            user_management.create_user(username, email, password, user_preferences, user_id)

    def test_create_blank_username(self):
        """Test that create_user raises UsernameCantBeBlank when the username is blank"""
        # Arrange
        username = ''
        email = 'email@example.com'
        password = 'password'
        user_preferences = {'preference': 'value'}
        user_id = 'new_user_id'
        mock_db_module = MagicMock()
        user_management = UserManagement(mock_db_module)
        # Act and Assert
        with self.assertRaises(UsernameCantBeBlank):
            user_management.create_user(username, email, password, user_preferences, user_id)

    def test_hash_password(self):
        """Test hashing a password"""
        password = "test_password"
        hashed_password = self.user_management.hash_password(password)
        self.assertTrue(bcrypt.checkpw(password.encode('utf-8'), hashed_password))

    def test_delete_user(self):
        """Test that delete_user calls delete_data with the correct arguments"""
        # Arrange
        user_id = 'existing_user_id'
        user_info = {'_id': user_id, 'username': 'username', 'email': 'email', 'schedules': []}
        user = User(**user_info)
        mock_db_module = MagicMock()
        mock_db_module.select_data.return_value = [user_info]
        user_management = UserManagement(mock_db_module)
        user_management.users[user_id] = user
        # Act
        user_management.delete_user(user_id)
        # Assert
        mock_db_module.delete_data.assert_called_once_with('users', {"_id": user_id})

    def test_delete_nonexistent_user(self):
        """Test that delete_user raises NonExistentIDError when the user does not exist"""
        # Arrange
        user_id = 'non_existent_user_id'
        mock_db_module = MagicMock()
        mock_db_module.select_data.return_value = []
        user_management = UserManagement(mock_db_module)

        # Act and Assert
        with self.assertRaises(NonExistentIDError):
            user_management.delete_user(user_id)

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

    # def test_add_schedule_to_user(self):
    #     """Test that add_schedule_to_user correctly adds a schedule to a user and updates the schedule's permissions"""
    #     # Arrange
    #     user_id = 'existing_user_id'
    #     other_user_id = 'other_user_id'
    #     schedule_id = 'new_schedule_id'
    #     permission = 'read'
    #     user_info = {'_id': user_id, 'username': 'username', 'email': 'email', 'schedules': []}
    #     user = User(**user_info)
    #     schedule = Schedule(schedule_id, 'title', 'description', {other_user_id: permission}, [])
    #     #schedule.set_title = MagicMock()  # Mock set_title
    #     mock_db_module = MagicMock()
    #     mock_db_module.select_data.return_value = [user_info]
    #     user_management = UserManagement(mock_db_module)
    #     user_management.users[user_id] = user
    #     mock_schedule_management = MagicMock()
    #     mock_schedule_management.get_schedule.return_value = schedule
    #     user_management.ScheduleManagement = mock_schedule_management

    #     # Act
    #     user_management.add_schedule_to_user(user_id, schedule_id, permission)

    #     # Assert
    #     self.assertIn(schedule_id, user.schedules)
    #     self.assertEqual(schedule.permissions[user_id], permission)

    def test_add_schedule_to_user_updates_user_schedules(self):
        """Test that add_schedule_to_user updates the user's schedules"""
        # Arrange
        user_id = 'existing_user_id'
        schedule_id = 'new_schedule_id'
        permission = 'read'
        mock_schedule = MagicMock()
        self.user_management.users[user_id] = User(user_id, 'username', 'email', [], {})
        user_info = {'_id': user_id, 'username': 'username', 'email': 'email', 'schedules': []}
        self.user_management.db_module.select_data.return_value = [user_info]  # Return a list so it can be subscripted
        with patch.object(ScheduleManagement, 'get_schedule', return_value=mock_schedule), \
            patch.object(UserManagement, 'user_exists', return_value=True):
            # Act
            self.user_management.add_schedule_to_user(user_id, schedule_id, permission)
            # Assert
            self.assertIn(schedule_id, self.user_management.users[user_id].schedules)

    def test_add_schedule_to_user_updates_schedules_permissions(self):
        """Test that add_schedule_to_user updates the schedule's permissions"""
        # Arrange
        user_id = 'existing_user_id'
        schedule_id = 'new_schedule_id'
        permission = 'read'
        mock_schedule = MagicMock()
        self.user_management.users[user_id] = User(user_id, 'username', 'email', [], {})
        user_info = {'_id': user_id, 'username': 'username', 'email': 'email', 'schedules': []}
        self.user_management.db_module.select_data.return_value = [user_info]  # Return a list so it can be subscripted
        with patch.object(ScheduleManagement, 'get_schedule', return_value=mock_schedule), \
            patch.object(UserManagement, 'user_exists', return_value=True):
            # Act
            self.user_management.add_schedule_to_user(user_id, schedule_id, permission)
            # Assert
            self.assertEqual(mock_schedule.permissions[user_id], permission)

    def test_add_schedule_to_nonexistant_user(self):
        """Test adding a schedule to a nonexistent user"""
        self.db_module.select_data = MagicMock(return_value = [])
        self.user_management.user_exists = MagicMock(return_value=False)
        with self.assertRaises(NonExistentIDError):
            self.user_management.add_schedule_to_user("id2", "test_schedule",
            "write")


if __name__ == '__main__':
    unittest.main()
