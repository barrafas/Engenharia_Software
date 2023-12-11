"""
Test file for schedule_management.py
"""

import unittest
from unittest.mock import Mock, MagicMock, patch

from src.calendar_elements.element_management import ElementManagement
from src.schedule.schedule_management import EmptyPermissionsError
from src.schedule.schedule_management import NonExistentIDError
from src.schedule.schedule_management import ScheduleManagement
from src.schedule.schedule_management import DuplicatedIDError
from src.user.user_management import UserManagement
from src.schedule.schedule_model import Schedule

class TestScheduleManagement(unittest.TestCase):
    """
    Test class for ScheduleManagement
    """

    def setUp(self):
        """Set up for the tests"""
        ScheduleManagement._instance = None

        self.db_module = MagicMock()

        self.schedules = {
            'schedule10': MagicMock(spec=Schedule),
        }

        self.schedule_management = ScheduleManagement.get_instance(
            self.db_module)
        ElementManagement._instance = None

        self.element_management = ElementManagement.get_instance(
            self.db_module)
        UserManagement._instance = None

        self.user_management = UserManagement.get_instance(self.db_module)

    def test_get_instance_creates_instance(self):
        """
        Test that get_instance creates an instance of ScheduleManagement
        """
        instance = ScheduleManagement.get_instance(self.db_module)
        self.assertIsInstance(instance, ScheduleManagement)

    def test_get_instance_returns_same_instance(self):
        """
        Test that get_instance always returns the same instance of ScheduleManagement
        """
        instance1 = ScheduleManagement.get_instance(self.db_module)
        instance2 = ScheduleManagement.get_instance(self.db_module)
        self.assertIs(instance1, instance2)

    def test_schedule_exists(self):
        """
        Test that schedule_exists returns True when the schedule exists
        """
        # Arrange
        self.db_module.select_data = MagicMock(return_value=[{'_id': 'schedule1',
                                                              'title': 'Schedule 1',
                                                              'description': 'This is schedule 1',
                                                              'permissions': {'user1': 'read', 'user2': 'write'},
                                                              'elements': ['element1', 'element2']
                                                              }])
        result = self.schedule_management.schedule_exists('schedule1')
        # Assert
        self.assertTrue(result)
        self.db_module.select_data.assert_called_with(
            'schedules', {'_id': 'schedule1'})

    def test_schedule_does_not_exist(self):
        """
        Test that schedule_exists returns False when the schedule does not exist
        """
        # Arrange
        self.db_module.select_data = MagicMock(return_value=[])
        result = self.schedule_management.schedule_exists('schedule1')
        # Assert
        self.assertFalse(result)
        self.db_module.select_data.assert_called_with(
            'schedules', {'_id': 'schedule1'})

    def test_create_schedule(self):
        """
        General test for create_schedule
        """
        # Arrange
        self.db_module.insert_data = MagicMock()
        self.db_module.select_data = MagicMock(return_value=[])
        schedule_id = "schedule10"
        title = "Schedule 2"
        description = "This is schedule 2"
        permissions = {"user1": "write", "user2": "read"}
        elements = ["element2", "element3"]
        mock_user = MagicMock()
        mock_element = MagicMock()
        with patch.object(self.user_management, 'get_user', return_value=mock_user), \
                patch.object(self.user_management, 'update_user', return_value=None), \
                patch.object(self.user_management, 'user_exists', return_value=True), \
                patch.object(self.element_management, 'get_element', return_value=mock_element), \
                patch.object(self.element_management, 'update_element', return_value=None), \
                patch.object(self.element_management, 'element_exists', return_value=True):

            result = self.schedule_management.create_schedule(schedule_id,
                                                              title,
                                                              description,
                                                              permissions,
                                                              elements)
            with self.subTest():
                self._test_create_schedule_insert_data(schedule_id,
                                                       title,
                                                       description,
                                                       permissions,
                                                       elements)
            with self.subTest():
                self._test_create_schedule_return(result)
            with self.subTest():
                self._test_create_schedule_attributes(result,
                                                      schedule_id,
                                                      title,
                                                      description,
                                                      permissions,
                                                      elements)
            with self.subTest():
                self._test_create_schedule_adds_to_self_schedules(schedule_id)
            with self.subTest():
                self._test_create_schedule_raises_error_if_schedule_exists(
                    schedule_id, title, description, permissions, elements)

    def _test_create_schedule_insert_data(self, schedule_id, title,
                                          description, permissions, elements):
        """ 
        Test for create_schedule insert_data
        """
        # Assert
        self.db_module.insert_data.assert_called_with('schedules',
                                                      {'_id': schedule_id,
                                                       'title': title,
                                                       'description': description,
                                                       'permissions': permissions,
                                                       'elements': elements})

    def _test_create_schedule_return(self, result):
        """
        Test for create_schedule return
        """
        # Assert
        self.assertIsInstance(result, Schedule)

    def _test_create_schedule_attributes(self, result, schedule_id, title,
                                         description, permissions, elements):
        """
        Test for create_schedule attributes
        """
        # Assert
        self.assertEqual(result.id, schedule_id)
        self.assertEqual(result.title, title)
        self.assertEqual(result.description, description)
        self.assertEqual(result.permissions, permissions)
        self.assertEqual(result.elements, elements)

    def _test_create_schedule_adds_to_self_schedules(self, schedule_id):
        """
        Test for create_schedule adds to self.schedules
        """
        # Assert
        self.assertIn(schedule_id, self.schedule_management.schedules)
        self.assertIsInstance(
            self.schedule_management.schedules[schedule_id], Schedule)

    def _test_create_schedule_raises_error_if_schedule_exists(self,
                                                              schedule_id,
                                                              title,
                                                              description,
                                                              permissions,
                                                              elements):
        """
        Test for create_schedule raises error if schedule exists
        """
        # Arrange
        self.schedule_management.schedule_exists = MagicMock(return_value=True)
        # Act & Assert
        with self.assertRaises(DuplicatedIDError):
            self.schedule_management.create_schedule(schedule_id, title,
                                                     description, permissions, elements)

    def test_create_schedule_raises_error_with_invalid_title(self):
        """
        Test that create_schedule raises an error when the title is invalid
        """
        # Arrange
        self.schedule_management.db_module.insert_data = MagicMock()
        self.schedule_management.db_module.select_data = MagicMock(
            return_value=[])
        invalid_titles = [None, 123, "", "   ",
                          "a" * 51]  # Covers all restrictions
        schedule_id = "schedule10"
        description = "This is schedule 2"
        permissions = {"user1": "write", "user2": "read"}
        elements = ["element2", "element3"]
        # Act & Assert
        with patch.object(self.user_management, 'user_exists', return_value=True), \
                patch.object(self.element_management, 'element_exists', return_value=True):
            for title in invalid_titles:
                with self.assertRaises((ValueError, TypeError)):
                    self.schedule_management.create_schedule(schedule_id,
                                                             title,
                                                             description,
                                                             permissions,
                                                             elements)

    def test_create_schedule_raises_error_with_invalid_description(self):
        """
        Test that create_schedule raises an error when the description is invalid
        """
        # Arrange
        self.schedule_management.db_module.insert_data = MagicMock()
        self.schedule_management.db_module.select_data = MagicMock(
            return_value=[])
        invalid_descriptions = [123, "a" * 501]  # Covers all restrictions
        schedule_id = "schedule10"
        title = "Schedule 2"
        permissions = {"user1": "write", "user2": "read"}
        elements = ["element2", "element3"]
        # Act & Assert
        with patch.object(self.user_management, 'user_exists', return_value=True), \
                patch.object(self.element_management, 'element_exists', return_value=True):
            for description in invalid_descriptions:
                with self.assertRaises((ValueError, TypeError)):
                    self.schedule_management.create_schedule(schedule_id, title,
                                                             description, permissions, elements)

    def test_create_schedule_raises_error_with_non_string_id(self):
        """
        Test that create_schedule raises an error when the ID is not a string
        """
        # Arrange
        self.schedule_management.db_module.insert_data = MagicMock()
        self.schedule_management.db_module.select_data = MagicMock(
            return_value=[])
        schedule_id = 123  # Non-string ID
        title = "Schedule 2"
        description = "This is schedule 2"
        permissions = {"user1": "write", "user2": "read"}
        elements = ["element2", "element3"]
        # Act & Assert
        with patch.object(self.user_management, 'user_exists', return_value=True), \
                patch.object(self.element_management, 'element_exists', return_value=True):
            with self.assertRaises(TypeError):
                self.schedule_management.create_schedule(schedule_id,
                                                         title,
                                                         description,
                                                         permissions,
                                                         elements)

    def test_create_schedule_raises_error_with_empty_permissions(self):
        """
        Test that create_schedule raises an error when the permissions are empty
        """
        # Arrange
        self.schedule_management.db_module.insert_data = MagicMock()
        self.schedule_management.db_module.select_data = MagicMock(
            return_value=[])
        schedule_id = "schedule10"
        title = "Schedule 2"
        description = "This is schedule 2"
        permissions = {}  # Empty permissions
        elements = ["element2", "element3"]
        # Act & Assert
        with patch.object(self.user_management, 'user_exists', return_value=True), \
                patch.object(self.element_management, 'element_exists', return_value=True):
            with self.assertRaises(EmptyPermissionsError):
                self.schedule_management.create_schedule(schedule_id,
                                                         title,
                                                         description,
                                                         permissions,
                                                         elements)

    def test_create_schedule_updates_elements(self):
        """
        Test that create_schedule updates the elements
        """
        # Arrange
        schedule_id = "schedule1"
        title = "Test Title"
        description = "Test Description"
        permissions = {"user1": {}}
        elements = ["element1", "element2", "element3"]
        mock_user = MagicMock()
        mock_element = MagicMock()
        mock_element.schedules = []

        with patch.object(self.user_management, 'user_exists', return_value=True), \
                patch.object(self.user_management, 'get_user', return_value=mock_user), \
                patch.object(self.element_management, 'element_exists', return_value=True), \
                patch.object(self.element_management, 'get_element', return_value=mock_element), \
                patch.object(self.schedule_management, 'schedule_exists', return_value=False):

            # Act
            self.schedule_management.create_schedule(
                schedule_id, title, description, permissions, elements)

            # Assert
            for _ in elements:
                self.assertIn(schedule_id, mock_element.schedules)

    def test_create_schedule_raises_error_for_nonexistent_element(self):
        """
        Test that create_schedule raises an error 
        when the element does not exist
        """
        # Arrange
        schedule_id = "schedule1"
        title = "Test Title"
        description = "Test Description"
        permissions = {"user1": {}}
        elements = ["element1", "nonexistent_element"]
        with patch.object(self.schedule_management, 'schedule_exists',
                          return_value=False), \
            patch.object(ElementManagement, 'element_exists',
                         side_effect=[True, False]):
            # Act & Assert
            with self.assertRaises(NonExistentIDError):
                self.schedule_management.create_schedule(schedule_id,
                                                         title,
                                                         description,
                                                         permissions,
                                                         elements)

    def test_create_schedule_updates_users(self):
        """
        Test that create_schedule updates the users
        """
        # Arrange
        schedule_id = "schedule1"
        title = "Test Title"
        description = "Test Description"
        permissions = {"user1": {}, "user2": {}, "user3": {}}
        elements = ["element1", "element2", "element3"]
        mock_element = MagicMock()
        mock_element.schedules = []
        mock_user = MagicMock()
        mock_user.schedules = []

        with patch.object(self.user_management, 'user_exists', return_value=True), \
                patch.object(self.user_management, 'get_user', return_value=mock_user), \
                patch.object(self.element_management, 'element_exists', return_value=True), \
                patch.object(self.element_management, 'get_element', return_value=mock_element), \
                patch.object(self.schedule_management, 'schedule_exists', return_value=False):

            # Act
            self.schedule_management.create_schedule(
                schedule_id, title, description, permissions, elements)

            # Assert
            for user_id in permissions:
                self.assertIn(schedule_id, mock_user.schedules)

    def test_create_schedule_raises_error_for_nonexistent_user(self):
        """
        Test that create_schedule raises an error when the user does not exist
        """
        # Arrange
        schedule_id = "schedule1"
        title = "Test Title"
        description = "Test Description"
        permissions = {"user1": {}, "nonexistent_user": {}}
        elements = ["element1", "element2"]
        with patch.object(self.schedule_management, 'schedule_exists',
                          return_value=False), \
            patch.object(UserManagement, 'user_exists',
                         side_effect=[True, False]):
            # Act & Assert
            with self.assertRaises(NonExistentIDError):
                self.schedule_management.create_schedule(schedule_id,
                                                         title,
                                                         description,
                                                         permissions,
                                                         elements)

    def test_get_schedule_id_exists_on_dict(self):
        """
        Check that get_schedule returns the correct schedule
        when the schedule exists in the dictionary
        """
        # Arrange
        schedule_id = "schedule10"
        title = "Schedule 2"
        description = "This is schedule 2"
        permissions = {"user1": "write", "user2": "read"}
        elements = ["element2", "element3"]
        schedule = Schedule(schedule_id, title, description, permissions,
                            elements)
        self.schedule_management.schedules[schedule_id] = schedule
        # Act
        result = self.schedule_management.get_schedule(schedule_id)
        # Assert
        self.assertEqual(result, schedule)

    def test_get_schedule_id_exists_in_database(self):
        """
        Check that get_schedule returns the correct schedule
        when the schedule exists in the database
        """
        # Arrange
        schedule_id = "schedule10"
        title = "Schedule 2"
        description = "This is schedule 2"
        permissions = {"user1": "write", "user2": "read"}
        elements = ["element2", "element3"]
        self.schedule_management.db_module.select_data = MagicMock(
            return_value=[{
                '_id': schedule_id,
                'title': title,
                'description': description,
                'permissions': permissions,
                'elements': elements
            }])
        self.schedule_management.schedule_exists = MagicMock(return_value=True)
        # Act
        result = self.schedule_management.get_schedule(schedule_id)
        # Assert
        self.assertEqual(result.title, title)
        self.assertEqual(result.description, description)
        self.assertEqual(result.permissions, permissions)
        self.assertEqual(result.elements, elements)

    def test_get_schedule_id_doesnt_exist(self):
        """
        Check that get_schedule raises an error when the schedule does not exist
        """
        # Arrange
        schedule_id = "schedule10"
        self.schedule_management.schedule_exists = MagicMock(
            return_value=False)
        # Act & Assert
        with self.assertRaises(NonExistentIDError):
            self.schedule_management.get_schedule(schedule_id)

    def test_update_schedule_id_exists(self):
        """
        Check that update_schedule updates the schedule when the schedule exists
        """
        # Arrange
        schedule_id = "schedule10"
        title = "Schedule 2"
        description = "This is schedule 2"
        permissions = {"user1": "write", "user2": "read"}
        elements = ["element2", "element3"]
        schedule = Schedule(schedule_id, title, description,
                            permissions, elements)
        self.schedule_management.schedules[schedule_id] = schedule
        self.schedule_management.db_module.update_data = MagicMock()
        # Act
        self.schedule_management.update_schedule(schedule_id)
        # Assert
        self.schedule_management.db_module.update_data.assert_called_once_with(
            'schedules',
            {'_id': schedule_id},
            schedule.to_dict()
        )

    def test_update_schedule_id_doesnt_exist(self):
        """
        Check that update_schedule raises an error 
        when the schedule does not exist
        """
        # Arrange
        schedule_id = "schedule10"
        self.schedule_management.schedule_exists = MagicMock(
            return_value=False)
        # Act & Assert
        with self.assertRaises(NonExistentIDError):
            self.schedule_management.update_schedule(schedule_id)

    def test_delete_schedule_deletes_from_database(self):
        """
        Check that delete_schedule deletes the schedule from the database
        """
        # Arrange
        schedule_id = "schedule10"
        self.schedule_management.db_module.delete_data = MagicMock()
        # Mock the return value of select_data
        self.schedule_management.db_module.select_data.return_value = [{
            '_id': schedule_id,
            'title': 'Test Title',
            'description': 'Test Description',
            'permissions': {},
            'elements': []
        }]
        # Act
        self.schedule_management.delete_schedule(schedule_id)
        # Assert
        self.schedule_management.db_module.delete_data.assert_called_once_with(
            'schedules', {'_id': schedule_id})

    def test_delete_schedule_deletes_schedule_from_dictionary(self):
        """
        Check that delete_schedule deletes the schedule from the dictionary
        """
        # Arrange
        schedule_id = "schedule10"
        self.schedule_management.schedules[schedule_id] = MagicMock()
        self.schedule_management.schedule_exists = MagicMock(return_value=True)
        self.schedule_management.db_module.delete_data = MagicMock()
        # Act
        self.schedule_management.delete_schedule(schedule_id)
        # Assert
        self.schedule_management.db_module.delete_data.assert_called_once_with(
            'schedules',
            {'_id': schedule_id}
        )
        self.assertNotIn(schedule_id, self.schedule_management.schedules)

    def test_delete_schedule_id_doesnt_exist(self):
        """
        Test that delete_schedule raises an error 
        when the schedule does not exist
        """
        # Arrange
        schedule_id = "schedule10"
        self.schedule_management.schedule_exists = MagicMock(
            return_value=False)
        # Act & Assert
        with self.assertRaises(NonExistentIDError):
            self.schedule_management.delete_schedule(schedule_id)

    def test_delete_schedule_updates_elements(self):
        """
        Test that delete_schedule updates the schedules of the elements
        """
        # Arrange
        schedule_id = "schedule1"
        element_ids = ["element1", "element2", "element3"]
        mock_schedule = MagicMock()
        mock_schedule.elements = element_ids
        self.schedule_management.schedules[schedule_id] = mock_schedule
        mock_element = MagicMock()
        mock_element.schedules = [schedule_id]

        with patch.object(self.schedule_management, 'get_schedule', return_value=mock_schedule), \
                patch.object(self.element_management, 'get_element', return_value=mock_element):

            # Act
            self.schedule_management.delete_schedule(schedule_id)

            # Assert
            for element_id in element_ids:
                self.assertNotIn(schedule_id, mock_element.schedules)

    def test_delete_schedule_updates_users(self):
        """
        Test that delete_schedule updates the schedules of the users
        """
        # Arrange
        schedule_id = "schedule1"
        user_ids = ["user1", "user2", "user3"]
        mock_schedule = MagicMock()
        mock_schedule.permissions = {user_id: {} for user_id in user_ids}
        self.schedule_management.schedules[schedule_id] = mock_schedule
        mock_user = MagicMock()
        mock_user.schedules = [schedule_id]

        with patch.object(self.schedule_management, 'get_schedule', return_value=mock_schedule), \
                patch.object(self.user_management, 'get_user', return_value=mock_user):

            # Act
            self.schedule_management.delete_schedule(schedule_id)

            # Assert
            for user_id in user_ids:
                self.assertNotIn(schedule_id, mock_user.schedules)

    def test_add_element_to_schedule_updates_schedule_elements(self):
        """
        Test that add_element_to_schedule updates the schedule's elements
        """
        # Arrange
        schedule_id = "schedule10"
        element_id = "element1"
        mock_element = MagicMock()
        self.schedule_management.schedules[schedule_id] = Schedule(schedule_id,
                                                                   "Title",
                                                                   "Description",
                                                                   {"user1": "read"},
                                                                   [])
        with patch.object(ElementManagement, 'get_element',
                          return_value=mock_element):
            # Act
            self.schedule_management.add_element_to_schedule(schedule_id,
                                                             element_id)
            # Assert
            self.assertIn(element_id,
                          self.schedule_management.schedules[schedule_id].elements)

    @patch.object(ElementManagement, 'get_instance')
    def test_add_element_to_schedule_invalid_element(self, mock_get_instance):
        """
        Test that add_element_to_schedule raises an error 
        when the element does not exist
        """
        # Arrange
        mock_element_manager = Mock()
        mock_element_manager.element_exists.return_value = False
        mock_get_instance.return_value = mock_element_manager
        schedule_id = "schedule1"
        element_id = "nonexistent_element"
        # Act & Assert
        with self.assertRaises(NonExistentIDError):
            self.schedule_management.add_element_to_schedule(schedule_id,
                                                             element_id)

    def test_add_element_to_schedule_invalid_schedule(self):
        """Test that add_element_to_schedule raises an error when the schedule
                does not exist"""
        # Arrange
        schedule_id = "nonexistent_schedule"
        element_id = "element1"
        self.schedule_management.schedule_exists = MagicMock(
            return_value=False)
        # Act & Assert
        with self.assertRaises(NonExistentIDError):
            self.schedule_management.add_element_to_schedule(schedule_id,
                                                             element_id)

    def test_add_element_to_schedule_duplicated_element(self):
        """
        Test that a error is raised when the element is already in the schedule
        """
        # Arrange
        schedule_id = "schedule1"
        element_id = "element1"
        self.schedule_management.schedules[schedule_id] = Schedule(schedule_id,
                                                                   "Title",
                                                                   "Description",
                                                                   {"user1": "read"},
                                                                   [element_id])
        self.schedule_management.schedule_exists = MagicMock(return_value=True)
        # Act & Assert
        with self.assertRaises(DuplicatedIDError):
            self.schedule_management.add_element_to_schedule(schedule_id,
                                                             element_id)

    def test_add_element_to_schedule_calls_update_schedule(self):
        """
        Test that add_element_to_schedule calls update_schedule
        """
        # Arrange
        schedule_id = "schedule1"
        element_id = "element1"
        mock_element = MagicMock()
        test_schedule = Schedule(schedule_id, "Title", "Description",
                                 {"user1": "read"}, ["element2"])
        test_schedule.attach(self.schedule_management)
        self.schedule_management.schedules[schedule_id] = test_schedule
        self.schedule_management.update = MagicMock()
        with patch.object(ElementManagement, 'get_element',
                          return_value=mock_element):
            # Act
            self.schedule_management.add_element_to_schedule(schedule_id,
                                                             element_id)
            # Assert
            self.schedule_management.update.assert_called_once_with(
                test_schedule)

    def test_add_element_to_schedule_updates_element_schedules(self):
        """
        Test that add_element_to_schedule updates the element's schedules
        """
        # Arrange
        schedule_id = "schedule10"
        element_id = "element1"

        # Create a mock schedule with 'element2' as an element
        mock_schedule = MagicMock(spec=Schedule)
        mock_schedule.elements = ["element2"]

        # Create a mock element with no schedules
        mock_element = MagicMock()
        mock_element.schedules = []

        # Mock the get_element method to return our mock element
        with patch.object(ElementManagement, 'get_element',
                          return_value=mock_element):
            # Add the mock schedule to the schedules dictionary
            self.schedule_management.schedules[schedule_id] = mock_schedule

            # Act
            self.schedule_management.add_element_to_schedule(schedule_id,
                                                             element_id)

            # Assert
            self.assertIn(schedule_id, mock_element.schedules)


if __name__ == '__main__': # pragma: no cover
    unittest.main() # pragma: no cover
