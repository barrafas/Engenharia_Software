import unittest
from src.schedule.schedule_management import ScheduleManagement
from unittest.mock import Mock

class TestScheduleManagement(unittest.TestCase):
    def setUp(self):
        # Reset the singleton instance before each test
        ScheduleManagement._instance = None
        self.db_module = Mock()

    def test_get_instance_creates_instance(self):
        instance = ScheduleManagement.get_instance(self.db_module)
        self.assertIsInstance(instance, ScheduleManagement)

    def test_get_instance_returns_same_instance(self):
        instance1 = ScheduleManagement.get_instance(self.db_module)
        instance2 = ScheduleManagement.get_instance(self.db_module)
        self.assertIs(instance1, instance2)

    

if __name__ == '__main__':
    unittest.main()