import unittest
from datetime import datetime, timedelta
from tests.test_users.mocks import Schedule, ScheduleManagement, Element, ElementManagement
from src.user.user_model import User
import bcrypt

class TestUserModel(unittest.TestCase):
    def setUp(self):
        # Set up for the tests

        # Create a  for ScheduleManagement and ElementManagement
        self.ScheduleManagement = ScheduleManagement()
        self.ElementManagement = ElementManagement()

    def test_get_all_elements(self):
        # Test getting all element ids from user schedules, without repetition
        user = User("id", "username", "email", ["id1", "id2"])
        result = user.get_elements()        
        self.assertEqual(sorted(result), ['elementid1', 'elementid2', 
                                  'elementid3', 'elementid4', 'elementid5'])


if __name__ == '__main__':
    unittest.main()
