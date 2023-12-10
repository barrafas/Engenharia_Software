import unittest
from src.calendar_elements.element_management import ElementManagement
from src.database.mongo_module import MongoModule
from src.database.database_module import DatabaseModule
from src.calendar_elements.element_factory import ElementFactory
from src.calendar_elements.element_interface import Element
from src.schedule.schedule_management import ScheduleManagement
from src.schedule.schedule_model import Schedule
from src.user.user_model import User
from src.user.user_management import UserManagement
from unittest.mock import Mock, MagicMock, patch

class TestElementManagement(unittest.TestCase):
    """ Tests for ElementManagement class """
    def setUp(self):
        # Reset singleton instance and create a mock database module
        ElementManagement._instance = None
        self.db_module = Mock(spec=MongoModule)
        self.element_management = ElementManagement.get_instance(self.db_module)

    def test_get_instance_creates_instance(self):
        """ Check that get_instance creates an instance of ElementManagement"""
        instance = ElementManagement.get_instance(self.db_module)
        self.assertIsInstance(instance, ElementManagement)

    def test_get_instance_returns_same_instance(self):
        """ Check that get_instance always returns the same instance of ElementManagement"""
        instance1 = ElementManagement.get_instance(self.db_module)
        instance2 = ElementManagement.get_instance(self.db_module)
        self.assertIs(instance1, instance2)

    def test_element_exists(self):
        """ Check that element_exists returns True if the element exists in the database """
        self.db_module.select_data = MagicMock(return_value={"_id": "id",
                                                                "title": "title",
                                                                "schedules": ["schedule1", "schedule2"],
                                                                "element_type": "event",
                                                                "start": "start",
                                                                "end": "end",
                                                                "description": "description"})
        result = self.element_management.element_exists("id")
        self.assertTrue(result)
        self.db_module.select_data.assert_called_with("elements", {"_id": "id"})

    def test_element_does_not_exist(self):
        """ Check that element_exists returns False if the element does not exist in the database """
        self.db_module.select_data = MagicMock(return_value=None)
        result = self.element_management.element_exists("id")
        self.assertFalse(result)
        self.db_module.select_data.assert_called_with("elements", {"_id": "id"})

    
if __name__ == '__main__':
    unittest.main()