import unittest
from datetime import datetime, timedelta
from tests.test_users.mocks import Schedule, ScheduleManagement, Element, ElementManagement
from src.user.user_model import User, UserNotInSchedule
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
        
    def test_get_filtered_elements(self):
        # Test getting all element ids from user schedules, with filter
        user = User("id", "username", "email", ["id1", "id2", "id3"])
        result = user.get_elements(["id1", "id3"])        
        self.assertEqual(sorted(result), ['elementid1', 'elementid2', 
                                    'elementid5', 'elementid6', 'elementid7'])
        
    def test_get_elements_from_schedule_user_isnt_in(self):
        # Test getting all element ids from a nonexistent schedule
        user = User("id", "username", "email", ["id1", "id2"])
        with self.assertRaises(UserNotInSchedule) as context:
            user.get_elements(["id3"])
        self.assertEqual(str(context.exception), 'Usuário não está nessa agenda')
        
    


if __name__ == '__main__':
    unittest.main()
