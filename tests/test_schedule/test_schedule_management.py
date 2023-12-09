import unittest
from src.schedule.schedule_management import ScheduleManagement
from src.schedule.schedule_model import Schedule
from unittest.mock import Mock, MagicMock

class TestScheduleManagement(unittest.TestCase):
    def setUp(self):
        # Reset the singleton instance before each test
        ScheduleManagement._instance = None
        self.db_module = Mock()
        self.schedule_management = ScheduleManagement.get_instance(self.db_module)

    def test_get_instance_creates_instance(self):
        instance = ScheduleManagement.get_instance(self.db_module)
        self.assertIsInstance(instance, ScheduleManagement)

    def test_get_instance_returns_same_instance(self):
        instance1 = ScheduleManagement.get_instance(self.db_module)
        instance2 = ScheduleManagement.get_instance(self.db_module)
        self.assertIs(instance1, instance2)

    def test_schedule_exists(self):
        # Arrange
        self.db_module.select_data = MagicMock(return_value=[{'_id': 'schedule1',\
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
        # Arrange
        self.db_module.select_data = MagicMock(return_value=[])
        result = self.schedule_management.schedule_exists('schedule1')
        # Assert
        self.assertFalse(result)
        self.db_module.select_data.assert_called_with('schedules', {'_id': 'schedule1'})
    
    def test_create_schedule(self):
        # Arrange
        self.db_module.insert_data = MagicMock()
        schedule_id = "schedule1"
        title = "Schedule 1"
        description = "This is schedule 1"
        permissions = {"user1": "read", "user2": "write"}
        elements = ["element1", "element2"]
        self._test_create_schedule_insert_data(schedule_id, title, description, permissions, elements)
        self._test_create_schedule_return(schedule_id, title, description, permissions, elements)
        self._test_create_schedule_attributes(schedule_id, title, description, permissions, elements)

    def _test_create_schedule_insert_data(self, schedule_id, title, description, permissions, elements):
        # Act
        result = self.schedule_management.create_schedule(schedule_id, title, description, permissions, elements)
        # Assert
        self.db_module.insert_data.assert_called_with('schedules', 
                                                      {'_id': schedule_id, 
                                                       'title': title, 
                                                       'description': description, 
                                                       'permissions': permissions,
                                                         'elements': elements})
        
    def _test_create_schedule_return(self, schedule_id, title, description, permissions, elements):
        # Act
        result = self.schedule_management.create_schedule(schedule_id, title, description, permissions, elements)
        # Assert
        self.assertIsInstance(result, Schedule)

    def _test_create_schedule_attributes(self, schedule_id, title, description, permissions, elements):
        # Act
        result = self.schedule_management.create_schedule(schedule_id, title, description, permissions, elements)
        # Assert
        self.assertEqual(result.id, schedule_id)
        self.assertEqual(result.title, title)
        self.assertEqual(result.description, description)
        self.assertEqual(result.permissions, permissions)
        self.assertEqual(result.elements, elements)
                                    

if __name__ == '__main__':
    unittest.main()