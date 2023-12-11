import unittest
from datetime import datetime, timedelta
from src.user.user_model import User, UserNotInSchedule, UsernameCantBeBlank, \
                                EmailCantBeBlank, TupleWithLessThanTwoDatetimeObjects
from unittest.mock import MagicMock
import bcrypt

class TestUserModel(unittest.TestCase):
    def setUp(self):
        # Set up for the tests
        # Create a  for ScheduleManagement and ElementManagement
        from src.schedule.schedule_management import ScheduleManagement
        from src.calendar_elements.element_management import ElementManagement
        self.database_module_mock = MagicMock()
        self.ScheduleManagement = ScheduleManagement.get_instance(self.database_module_mock)
        self.ElementManagement = ElementManagement.get_instance(self.database_module_mock)

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
        with self.assertRaises(UserNotInSchedule):
            user.get_elements(["id3"])
        
    def test_set_username(self):
        # Test setting a username
        user = User("id", "username", "email", ["id1", "id2"])
        user.set_username("new_username")
        self.assertEqual(user.username, "new_username")
        
    def test_set_username_with_trailing_space(self):
        # Test setting a username with trailing space
        user = User("id", "username", "email", ["id1", "id2"])
        user.set_username("new_username ")
        self.assertEqual(user.username, "new_username")

    def test_set_username_with_int(self):
        # Test setting a username with trailing space
        user = User("id", "username", "email", ["id1", "id2"])
        with self.assertRaises(TypeError):
            user.set_username(123)

        
    def test_set_blank_username(self):
        # Test setting a blank username
        user = User("id", "username", "email", ["id1", "id2"])
        with self.assertRaises(UsernameCantBeBlank):
            user.set_username("")
        
    def test_set_email(self):
        # Test setting an email
        user = User("id", "username", "email", ["id1", "id2"])
        user.set_email("new_email")
        self.assertEqual(user.email, "new_email")

    def test_set_email_with_trailing_space(self):
        # Test setting an email with trailing space
        user = User("id", "username", "email", ["id1", "id2"])
        user.set_email("new_email ")
        self.assertEqual(user.email, "new_email")

    def test_set_email_with_int(self):
        # Test setting an email with trailing space
        user = User("id", "username", "email", ["id1", "id2"])
        with self.assertRaises(TypeError):
            user.set_email(123)
        
    def test_set_blank_email(self):
        # Test setting a blank email
        user = User("id", "username", "email", ["id1", "id2"])
        with self.assertRaises(EmailCantBeBlank):
            user.set_email("")
        
    def test_set_preference(self):
        # Test setting a preference
        user = User("id", "username", "email", ["id1", "id2"])
        user.set_preferences({"preference_type": "preference"})
        self.assertEqual(user.user_preferences["preference_type"], "preference")
            
    def test_set_preference_with_int(self):
        user = User("id", "username", "email", ["id1", "id2"])
        with self.assertRaises(TypeError):
            user.set_preferences({123: 'preference'})

    def test_check_disponibility(self):
        user = User("id", "username", "email", ["id1", "id2"])
        time = (datetime.now() + timedelta(hours=2), 
                datetime.now() + timedelta(hours=3))
        
        self.ElementManagement.create_element = MagicMock()
        self.ElementManagement.get_element = MagicMock(return_value=self.ElementManagement.get_element("elementid1"))
        result = user.check_disponibility(time)
        self.assertTrue(result)

    def test_check_disponibility_end_time_same_as_other_event_start_time(self):
        user = User("id", "username", "email", ["id1", "id2"])
        time = (datetime.now() + timedelta(hours=11), 
                self.ElementManagement.get_element("elementid5").start_time)
        result = user.check_disponibility(time)
        self.assertTrue(result)

    def test_check_disponibility_ignoring_non_event_elements(self):
        user = User("id", "username", "email", ["id1", "id2"])
        time = (self.ElementManagement.get_element("elementid3").start_time,
                self.ElementManagement.get_element("elementid3").end_time)
        result = user.check_disponibility(time)
        self.assertTrue(result)

    def test_check_disponibility_input_type_exception(self):
        user = User("id", "username", "email", ["id1", "id2"])
        time = "time"
        with self.assertRaises(TypeError):
            user.check_disponibility(time)

    def test_check_disponibility_not_datetime(self):
        user = User("id", "username", "email", ["id1", "id2"])
        time = (123, 123)
        with self.assertRaises(TypeError):
            user.check_disponibility(time)
        
    def test_check_disponibility_short_tuple(self):
        user = User("id", "username", "email", ["id1", "id2"])
        time = (datetime.now(),)
        with self.assertRaises(TupleWithLessThanTwoDatetimeObjects):
            user.check_disponibility(time)

if __name__ == '__main__':
    unittest.main()
