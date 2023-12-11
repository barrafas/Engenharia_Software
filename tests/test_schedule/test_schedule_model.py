import unittest
from src.schedule.schedule_model import Schedule
#from tests.test_schedule.mocks import Element, User
from unittest.mock import MagicMock, PropertyMock, patch
from src.schedule.schedule_management import ScheduleManagement
from src.user.user_model import User
from src.user.user_management import UserManagement
from src.calendar_elements.element_interface import Element
from src.calendar_elements.element_management import ElementManagement
from typing import Optional

class TestScheduleModel(unittest.TestCase):

    def setUp(self):
        # Set up for the tests
        db_module_mocl = MagicMock()
        # initialize the management classes
        ElementManagement.get_instance(database_module=db_module_mocl)
        UserManagement.get_instance(database_module=db_module_mocl)
        ScheduleManagement.get_instance(database_module=db_module_mocl)

        self.id = "schedule_id"
        self.title = "schedule_title"
        self.description = "schedule_description"
        self.permissions = {"user_id1": "permission_type1", 
                            "user_id2": "permission_type2",
                            "user_id3": "permission_type1"}
        self.elements = ["element1", "element2"]

        self.schedule = Schedule(self.id, self.title, self.description, self.permissions, self.elements)

        # Access private attributes for testing
        self.schedule._Schedule__id = self.id
        self.schedule._Schedule__permissions = self.permissions
        self.schedule._Schedule__elements = self.elements

    def test_id_property(self):
        # Test the id property
        self.assertEqual(self.schedule.id, self.id)

    def test_permissions_property(self):
        # Test the permissions property
        self.assertEqual(self.schedule.permissions, self.permissions)

    def test_elements_property(self):
        # Test the elements property
        self.assertEqual(self.schedule.elements, self.elements)

    def test_set_title_valid(self):
        # Test setting a valid title
        valid_title = "Valid Title"
        self.schedule.set_title(valid_title)
        self.assertEqual(self.schedule.title, valid_title)

    def test_set_title_not_string(self):
        # Test setting a title that is not a string
        with self.assertRaises(TypeError):
            self.schedule.set_title(123)

    def test_set_title_none(self):
        # Test setting a title that is None
        with self.assertRaises(ValueError):
            self.schedule.set_title(None)

    def test_set_title_too_long(self):
        # Test setting a title that is too long
        with self.assertRaises(ValueError):
            self.schedule.set_title("a" * 51)
    
    def test_set_title_max_length(self):
        # Test setting a title that is exactly at the maximum length
        max_length_title = "a" * 50
        self.schedule.set_title(max_length_title)
        self.assertEqual(self.schedule.title, max_length_title)
    
    def test_set_title_whitespace(self):
        # Test setting a title that contains only whitespace
        with self.assertRaises(ValueError):
            self.schedule.set_title("   ")

    def test_set_title_empty(self):
        # Test setting an empty title
        with self.assertRaises(ValueError):
            self.schedule.set_title("")

    def test_set_description_valid(self):
        # Test setting a valid description
        valid_description = "Valid Description"
        self.schedule.set_description(valid_description)
        self.assertEqual(self.schedule.description, valid_description)

    def test_set_description_not_string(self):
        # Test setting a description that is not a string
        with self.assertRaises(TypeError):
            self.schedule.set_description(123)

    def test_set_description_none(self):
        # Test setting a description that is None
        self.schedule.set_description(None)
        self.assertEqual(self.schedule.description, None)

    def test_set_description_too_long(self):
        # Test setting a description that is too long
        with self.assertRaises(ValueError):
            self.schedule.set_description("a" * 501)

    def test_set_description_max_length(self):
        # Test setting a description that is exactly at the maximum length
        max_length_description = "a" * 500
        self.schedule.set_description(max_length_description)
        self.assertEqual(self.schedule.description, max_length_description)

    def test_to_dict(self):
        # Call the to_dict method
        schedule_dict = self.schedule.to_dict()

        # Check that the dictionary has the correct keys and values
        self.assertEqual(schedule_dict, {
            "_id": self.id,
            "title": self.title,
            "description": self.description,
            "permissions": self.permissions,
            "elements": self.elements
        })

    def test_to_dict_permissions(self):
        # Test that to_dict correctly converts permissions
        schedule_dict = self.schedule.to_dict()
        self.assertEqual(schedule_dict["permissions"], self.permissions)

    def test_to_dict_elements(self):
        # Test that to_dict correctly converts elements
        schedule_dict = self.schedule.to_dict()
        self.assertEqual(schedule_dict["elements"], self.elements)

    def test_to_dict_none_empty(self):
        # Test to_dict when attributes are None or empty
        empty_schedule = Schedule(self.id, self.title, None, {'userid1': 'permissiontype1'}, [])
        schedule_dict = empty_schedule.to_dict()
        self.assertEqual(schedule_dict, {
            "_id": self.id,
            "title": self.title,
            "description": None,
            "permissions": {'userid1': 'permissiontype1'},
            "elements": []
        })

    def test_get_elements(self):
        # Test that get_elements returns the correct elements
        element_management = ElementManagement.get_instance()
        schedule = Schedule('id', 'title', 'description', {'userid1': 'permissiontype1'}, ['elementid1', 'elementid2'])
        elements = schedule.get_elements()
        expected_elements = [element_management.elements['elementid1'], element_management.elements['elementid2']]
        self.assertEqual(elements, expected_elements)

    def test_get_elements_with_types(self):
        # Test that get_elements returns the correct elements with the specified types
        element_management = ElementManagement.get_instance()
        schedule = Schedule('id', 'title', 'description', {'userid1': 'permissiontype1'}, ['elementid1', 'elementid2', 'elementid3', 'elementid4'])
        elements = schedule.get_elements(['evento'])
        expected_elements = [element_management.elements['elementid1'], element_management.elements['elementid4']]
        self.assertEqual(elements, expected_elements)

    def test_get_elements_empty(self):
        # Test that get_elements returns an empty list when there are no elements
        schedule = Schedule('id', 'title', 'description', {'userid1': 'permissiontype1'}, [])
        elements = schedule.get_elements()
        self.assertEqual(elements, [])
    
    def test_get_elements_nonexistent_type(self):
        # Test that get_elements returns an empty list when there are no elements with the specified type
        schedule = Schedule('id', 'title', 'description', {'userid1': 'permissiontype1'}, ['elementid1', 'elementid2', 'elementid3', 'elementid4'])
        elements = schedule.get_elements(['citrico'])
        self.assertEqual(elements, [])

    # def test_get_users(self):
    #     # Test that get_users returns the correct users
    #     user_management = UserManagement.get_instance()
    #     schedule = Schedule('id', 'title', 'description', {'userid1': 'permissiontype1', 'userid2': 'permissiontype2'}, [])
    #     users = schedule.get_users()
    #     expected_users = [user_management.users['userid1'], user_management.users['userid2']]
    #     self.assertEqual(users, expected_users)

    def test_get_users(self):
        """Test that get_users returns the correct users"""
        # Arrange
        schedule = Schedule("schedule1", "Test Title", "Test Description",
         {"user1": "read", "user2": "write", "user3": "read"}, ["element1"])
        user_ids = ["user1", "user2", "user3"]
        mock_user = MagicMock()
        mock_user_management = MagicMock()
        mock_user_management.get_user.return_value = mock_user

        with patch.object(UserManagement, 'get_instance', return_value=mock_user_management):

            # Act
            users = schedule.get_users()

            # Assert
            self.assertEqual(len(users), len(user_ids))
            for user in users:
                self.assertEqual(user, mock_user)


    def test_get_users_with_permission_types(self):
        """Test that get_users returns the correct users with the specified permission types"""
        # Arrange
        schedule = Schedule("schedule1", "Test Title", "Test Description",
                            {"user1": "type1", "user2": "type2", "user3": "type1"}, ["element1"])
        user_ids = ["user1", "user3"]
        mock_user = MagicMock()
        mock_user_management = MagicMock()
        mock_user_management.get_user.return_value = mock_user

        with patch.object(UserManagement, 'get_instance', return_value=mock_user_management):

            # Act
            users = schedule.get_users(['type1'])

            # Assert
            self.assertEqual(len(users), len(user_ids))
            for user in users:
                self.assertEqual(user, mock_user)

    # Cancelled test because it is not possible to have empty users
    #def test_get_users_empty(self):
    #    # Test that get_users returns an empty list when there are no users
    #    schedule = Schedule('id', 'title', 'description', [], [])
    #    users = schedule.get_users()
    #    self.assertEqual(users, [])

    def test_get_users_nonexistent_permission_type(self):
        # Test that get_users returns an empty list when there are no users with the specified permission type
        schedule = Schedule('id', 'title', 'description', {'userid1': 'permissiontype1', 'userid2': 'permissiontype2', 'userid3': 'permissiontype1'}, [])
        users = schedule.get_users(['permissiontype3'])
        self.assertEqual(users, [])

    def test_elements_setter_accepts_valid_input(self):
        # Arrange
        schedule = Schedule("schedule1", "Title", "Description", {"user1": "read"}, ["element1"])
        new_elements = ["element2", "element3"]
        # Act
        schedule.elements = new_elements
        # Assert
        self.assertEqual(schedule.elements, new_elements)

    def test_elements_setter_raises_error_on_invalid_input(self):
        # Arrange
        schedule = Schedule("schedule1", "Title", "Description", {"user1": "read"}, ["element1"])
        invalid_elements = "element2"
        # Act & Assert
        with self.assertRaises(ValueError):
            schedule.elements = invalid_elements

    def test_changes_on_elements_calls_schedule_management_update_schedule(self):
        # Arrange
        schedule = Schedule("schedule1", "Title", "Description", {"user1": "read"}, ["element1"])
        schedule_management = ScheduleManagement.get_instance(database_module=MagicMock())
        schedule_management.update_schedule = MagicMock()
        schedule.attach(schedule_management)
        # Act
        schedule.elements = ["changed_element1"]
        # Assert
        schedule_management.update_schedule.assert_called_once_with("schedule1")

    def get_mock_user(self) -> tuple[callable, MagicMock, MagicMock, MagicMock, MagicMock]:
        """Mock function to return a user object"""

        # Set up the mock objects
        user_1 = MagicMock(spec=User)
        type(user_1).id = PropertyMock(return_value='user_1')
        type(user_1).username = PropertyMock(return_value='user_1')
        type(user_1).schedules = PropertyMock(return_value=['schedule_1', 'schedule_2'])

        user_2 = MagicMock(spec=User)
        type(user_2).id = PropertyMock(return_value='user_2')
        type(user_2).username = PropertyMock(return_value='user_2')
        type(user_2).schedules = PropertyMock(return_value=['schedule_1'])

        user_3 = MagicMock(spec=User)
        type(user_3).id = PropertyMock(return_value='user_3')
        type(user_3).username = PropertyMock(return_value='user_3')
        type(user_3).schedules = PropertyMock(return_value=['schedule_2'])

        user_4 = MagicMock(spec=User)
        type(user_4).id = PropertyMock(return_value='user_4')
        type(user_4).username = PropertyMock(return_value='user_4')
        type(user_4).schedules = PropertyMock(return_value=[])

        def get_user_mock(id: str) -> Optional[MagicMock]:
            return {
                'user_1': user_1,
                'user_2': user_2,
                'user_3': user_3,
                'user_4': user_4
            }.get(id, None)

        return get_user_mock, user_1, user_2, user_3, user_4

if __name__ == '__main__':
    unittest.main()
