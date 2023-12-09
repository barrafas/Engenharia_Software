import unittest
from src.schedule.schedule_management import ScheduleManagement
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
        self.db_module.select_data = MagicMock(return_value=[{'_id': 'schedule1',\
                                                               'title': 'Schedule 1',\
                                                                'description': 'This is schedule 1',\
                                                                'permissions': {'user1': 'read', 'user2': 'write'},\
                                                                'elements': ['element1', 'element2']
                                                               }])
        result = self.schedule_management.schedule_exists('schedule1')
        self.assertTrue(result)
        self.db_module.select_data.assert_called_with('schedules', {'_id': 'schedule1'})

    def test_schedule_does_not_exist(self):
        self.db_module.select_data = MagicMock(return_value=[])
        result = self.schedule_management.schedule_exists('schedule1')
        self.assertFalse(result)
        self.db_module.select_data.assert_called_with('schedules', {'_id': 'schedule1'})
    

if __name__ == '__main__':
    unittest.main()