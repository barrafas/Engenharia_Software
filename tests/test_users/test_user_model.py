import unittest
from datetime import datetime, timedelta
from tests.test_users.mocks import Schedule, ScheduleManagement, Element, ElementManagement
from src.user.user_model import User, UserNotInSchedule, UsernameCantBeBlank, \
                                EmailCantBeBlank
import bcrypt

class TestUserModel(unittest.TestCase):
    def setUp(self):
        # Set up for the tests

        # Create a  for ScheduleManagement and ElementManagement
        self.ScheduleManagement = ScheduleManagement.get_instance()
        self.ElementManagement = ElementManagement.get_instance()

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
        self.assertEqual(str(context.exception), 
                         'Usuário não está nessa agenda: id3')
        
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
        with self.assertRaises(TypeError) as context:
            user.set_username(123)
        self.assertEqual(str(context.exception), 
                         "O nome de usuário deve ser uma string")
        
    def test_set_blank_username(self):
        # Test setting a blank username
        user = User("id", "username", "email", ["id1", "id2"])
        with self.assertRaises(UsernameCantBeBlank) as context:
            user.set_username("")
        self.assertEqual(str(context.exception), 
                         "O nome de usuário não pode ser vazio")
        
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
        with self.assertRaises(TypeError) as context:
            user.set_email(123)
        self.assertEqual(str(context.exception), 
                         "O email deve ser uma string")
        
    def test_set_blank_email(self):
        # Test setting a blank email
        user = User("id", "username", "email", ["id1", "id2"])
        with self.assertRaises(EmailCantBeBlank) as context:
            user.set_email("")
        self.assertEqual(str(context.exception), 
                         "O email não pode ser vazio")
        
    def test_check_disponibility(self):
        user = User("id", "username", "email", ["id1", "id2"])
        time = (datetime.now() + timedelta(hours=2), 
                datetime.now() + timedelta(hours=3))
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
        with self.assertRaises(TypeError) as context:
            user.check_disponibility(time)
        self.assertEqual(str(context.exception), 
                         "O horário deve ser uma tupla")


if __name__ == '__main__':
    unittest.main()
