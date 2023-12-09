import unittest
from src.schedule.schedule_management import ScheduleManagement
from src.schedule.schedule_management import EmptyPermissionsError, DuplicatedIDError, NonExistentIDError
from src.schedule.schedule_model import Schedule
from unittest.mock import Mock, MagicMock

class TestScheduleManagement(unittest.TestCase):
    def setUp(self):
        # Reset the singleton instance before each test
        ScheduleManagement._instance = None
        self.db_module = Mock()
        self.schedule_management = ScheduleManagement.get_instance(self.db_module)

    def test_get_instance_creates_instance(self):
        # Check that get_instance creates an instance of ScheduleManagement
        instance = ScheduleManagement.get_instance(self.db_module)
        self.assertIsInstance(instance, ScheduleManagement)

    def test_get_instance_returns_same_instance(self):
        # Check that get_instance always returns the same instance of ScheduleManagement
        instance1 = ScheduleManagement.get_instance(self.db_module)
        instance2 = ScheduleManagement.get_instance(self.db_module)
        self.assertIs(instance1, instance2)

    def test_schedule_exists(self):
        # Check that schedule_exists returns True when the schedule exists
        # Arrange
        self.db_module.select_data = MagicMock(return_value = [{'_id': 'schedule1',\
                                                               'title': 'Schedule 1',\
                                                                'description': 'This is schedule 1',\
                                                                'permissions': {'user1': 'read', 'user2': 'write'},\
                                                                'elements': ['element1', 'element2']
                                                               }])
        result = self.schedule_management.schedule_exists('schedule1')
        # Assert
        self.assertTrue(result)
        self.db_module.select_data.assert_called_with('schedules', {'_id': 'schedule1'})

    def test_schedule_does_not_exist(self):
        # Check that schedule_exists returns False when the schedule does not exist
        # Arrange
        self.db_module.select_data = MagicMock(return_value=[])
        result = self.schedule_management.schedule_exists('schedule1')
        # Assert
        self.assertFalse(result)
        self.db_module.select_data.assert_called_with('schedules', {'_id': 'schedule1'})
    
    def test_create_schedule(self):
        # General test for create_schedule
        # Arrange
        self.db_module.insert_data = MagicMock()
        self.db_module.select_data = MagicMock(return_value=[])
        schedule_id = "schedule10"
        title = "Schedule 2"
        description = "This is schedule 2"
        permissions = {"user1": "write", "user2": "read"}
        elements = ["element2", "element3"]
        # Act
        result = self.schedule_management.create_schedule(schedule_id, title, description, permissions, elements)
        with self.subTest("Test insert_data is called with correct arguments"):
            self._test_create_schedule_insert_data(schedule_id, title, description, permissions, elements)
        with self.subTest("Test create_schedule returns a Schedule instance"):
            self._test_create_schedule_return(result)
        with self.subTest("Test Schedule instance has correct attributes"):
            self._test_create_schedule_attributes(result, schedule_id, title, description, permissions, elements)
        with self.subTest("Test create_schedule adds to self.schedules"):
            self._test_create_schedule_adds_to_self_schedules(schedule_id)
        with self.subTest("Test create_schedule raises error if schedule exists"):
            self._test_create_schedule_raises_error_if_schedule_exists(schedule_id, title, description, permissions, elements)

    def _test_create_schedule_insert_data(self, schedule_id, title, description, permissions, elements):
        # Assert
        self.db_module.insert_data.assert_called_with('schedules', 
                                                      {'_id': schedule_id, 
                                                       'title': title, 
                                                       'description': description, 
                                                       'permissions': permissions,
                                                         'elements': elements})
        
    def _test_create_schedule_return(self, result):
        # Assert
        self.assertIsInstance(result, Schedule)

    def _test_create_schedule_attributes(self, result, schedule_id, title, description, permissions, elements):
        # Assert
        self.assertEqual(result.id, schedule_id)
        self.assertEqual(result.title, title)
        self.assertEqual(result.description, description)
        self.assertEqual(result.permissions, permissions)
        self.assertEqual(result.elements, elements)

    def _test_create_schedule_adds_to_self_schedules(self, schedule_id):
        # Assert
        self.assertIn(schedule_id, self.schedule_management.schedules)
        self.assertIsInstance(self.schedule_management.schedules[schedule_id], Schedule)

    def _test_create_schedule_raises_error_if_schedule_exists(self, schedule_id, title, description, permissions, elements):
        # Arrange
        self.schedule_management.schedule_exists = MagicMock(return_value=True)
        # Act & Assert
        with self.assertRaises(DuplicatedIDError):
            self.schedule_management.create_schedule(schedule_id, title, description, permissions, elements)

    def test_create_schedule_raises_error_with_invalid_title(self):
        # Check that create_schedule raises an error when the title is invalid
        # Arrange
        self.schedule_management.db_module.insert_data = MagicMock()
        self.schedule_management.db_module.select_data = MagicMock(return_value=[])
        invalid_titles = [None, 123, "", "   ", "a" * 51]  # Covers all restrictions
        schedule_id = "schedule10"
        description = "This is schedule 2"
        permissions = {"user1": "write", "user2": "read"}
        elements = ["element2", "element3"]
        # Act & Assert
        for title in invalid_titles:
            with self.assertRaises((ValueError, TypeError)):
                self.schedule_management.create_schedule(schedule_id, title, description, permissions, elements)

    def test_create_schedule_raises_error_with_invalid_description(self):
        # Check that create_schedule raises an error when the description is invalid
        # Arrange
        self.schedule_management.db_module.insert_data = MagicMock()
        self.schedule_management.db_module.select_data = MagicMock(return_value=[])
        invalid_descriptions = [123, "a" * 501]  # Covers all restrictions
        schedule_id = "schedule10"
        title = "Schedule 2"
        permissions = {"user1": "write", "user2": "read"}
        elements = ["element2", "element3"]
        # Act & Assert
        for description in invalid_descriptions:
            with self.assertRaises((ValueError, TypeError)):
                self.schedule_management.create_schedule(schedule_id, title, description, permissions, elements)

    def test_create_schedule_raises_error_with_non_string_id(self):
        # Check that create_schedule raises an error when the ID is not a string
        # Arrange
        self.schedule_management.db_module.insert_data = MagicMock()
        self.schedule_management.db_module.select_data = MagicMock(return_value=[])
        schedule_id = 123  # Non-string ID
        title = "Schedule 2"
        description = "This is schedule 2"
        permissions = {"user1": "write", "user2": "read"}
        elements = ["element2", "element3"]
        # Act & Assert
        with self.assertRaises(TypeError):
            self.schedule_management.create_schedule(schedule_id, title, description, permissions, elements)

    def test_create_schedule_raises_error_with_empty_permissions(self):
        # Check that create_schedule raises an error when the permissions are empty
        # Arrange
        self.schedule_management.db_module.insert_data = MagicMock()
        self.schedule_management.db_module.select_data = MagicMock(return_value=[])
        schedule_id = "schedule10"
        title = "Schedule 2"
        description = "This is schedule 2"
        permissions = {}  # Empty permissions
        elements = ["element2", "element3"]
        # Act & Assert
        with self.assertRaises(EmptyPermissionsError):
            self.schedule_management.create_schedule(schedule_id, title, description, permissions, elements)

    def test_get_schedule_id_exists_on_dict(self):
        # Check that get_schedule returns the correct schedule when the schedule exists in the dictionary
        # Arrange
        schedule_id = "schedule10"
        title = "Schedule 2"
        description = "This is schedule 2"
        permissions = {"user1": "write", "user2": "read"}
        elements = ["element2", "element3"]
        schedule = Schedule(schedule_id, title, description, permissions, elements)
        self.schedule_management.schedules[schedule_id] = schedule
        # Act
        result = self.schedule_management.get_schedule(schedule_id)
        # Assert
        self.assertEqual(result, schedule)

    def test_get_schedule_id_exists_in_database(self):
        # Check that get_schedule returns the correct schedule when the schedule exists in the database
        # Arrange
        schedule_id = "schedule10"
        title = "Schedule 2"
        description = "This is schedule 2"
        permissions = {"user1": "write", "user2": "read"}
        elements = ["element2", "element3"]
        self.schedule_management.db_module.select_data = MagicMock(return_value={
            '_id': schedule_id, 
            'title': title, 
            'description': description, 
            'permissions': permissions, 
            'elements': elements
        })
        self.schedule_management.schedule_exists = MagicMock(return_value=True)
        # Act
        result = self.schedule_management.get_schedule(schedule_id)
        # Assert
        self.assertEqual(result.title, title)
        self.assertEqual(result.description, description)
        self.assertEqual(result.permissions, permissions)
        self.assertEqual(result.elements, elements)

    def test_get_schedule_id_doesnt_exist(self):
        # Check that get_schedule raises an error when the schedule does not exist
        # Arrange
        schedule_id = "schedule10"
        self.schedule_management.schedule_exists = MagicMock(return_value=False)
        # Act & Assert
        with self.assertRaises(NonExistentIDError):
            self.schedule_management.get_schedule(schedule_id)

    def test_update_schedule_id_exists(self):
        # Check that update_schedule updates the schedule when the schedule exists
        # Arrange
        schedule_id = "schedule10"
        title = "Schedule 2"
        description = "This is schedule 2"
        permissions = {"user1": "write", "user2": "read"}
        elements = ["element2", "element3"]
        schedule = Schedule(schedule_id, title, description, permissions, elements)
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
        # Check that update_schedule raises an error when the schedule does not exist
        # Arrange
        schedule_id = "schedule10"
        self.schedule_management.schedule_exists = MagicMock(return_value=False)
        # Act & Assert
        with self.assertRaises(NonExistentIDError):
            self.schedule_management.update_schedule(schedule_id)

    def test_delete_schedule_deletes_from_database(self):
        # Check that delete_schedule deletes the schedule from the database
        # Arrange
        schedule_id = "schedule10"
        self.schedule_management.db_module.delete_data = MagicMock()
        # Act
        self.schedule_management.delete_schedule(schedule_id)
        # Assert
        self.schedule_management.db_module.delete_data.assert_called_once_with(
            'schedules', 
            {'_id': schedule_id}
        )


if __name__ == '__main__':
    unittest.main()