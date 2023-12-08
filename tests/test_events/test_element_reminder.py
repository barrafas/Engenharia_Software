import unittest
from datetime import datetime, timedelta
from src.calendar_elements.element_types import ReminderElement
from tests.test_events.mocks import Schedule, ScheduleManagement, User, UserManagement

class TestReminderElement(unittest.TestCase):

    def setUp(self):
        self.id = "1"
        self.title = "Test Reminder"
        self.description = "Description"
        self.reminder_date = datetime(2023, 1, 1)
        self.schedules = ['schedule_1', 'schedule_2']
        self.type = "reminder"
        self.reminder = ReminderElement(self.id, self.title, self.reminder_date, 
                                        self.description, self.schedules, self.type)
        
        # Access private attributes for testing
        self.reminder._ReminderElement__id = self.id
        self.reminder._ReminderElement__type = self.type
        self.reminder._ReminderElement__schedules = self.schedules

    def test_id_property(self):
        # Test the id property
        self.assertEqual(self.reminder.id, self.id)

    def test_type_property(self):
        # Test the schedules property
        self.assertEqual(self.reminder.type, self.type)
    
    def test_schedules_property(self):
        # Test the schedules property
        self.assertEqual(self.reminder.schedules, self.schedules)

    def test_get_display_interval(self):
        # Verify if the interval returned matches the one that was set in 
        # the constructor
        expected_interval = (datetime(2022, 12, 31, 23, 50), datetime(2023, 1, 1))
        print(self.reminder.get_display_interval())
        self.assertEqual(self.reminder.get_display_interval(), expected_interval)

    def test_get_type(self):
        # Verify if the type returned is "reminder"
        self.assertEqual(self.reminder.get_type(), "reminder")

    def test_get_schedules(self):
        # Verify if the schedules returned match the ones that were set in
        # the constructor
        schedule_management = ScheduleManagement.get_instance()
        reminder = ReminderElement(self.id, self.title, self.reminder_date, self.description, 
                             ['id1', 'id2', 'id3'])
        schedules = reminder.get_schedules()
        expected_schedule = [schedule_management.get_schedule(id) for id in ['id1', 'id2', 'id3']]
        self.assertEqual(schedules, expected_schedule)

    def test_get_schedules_empty(self):
        pass

    def test_get_users(self):
        pass

    def test_get_users_empty(self):
        pass

    def test_get_users_with_filter_by_schedules(self):
        pass

    def test_set_reminder_date_valid(self):
        # Test setting a valid reminder date
        valid_reminder_date = datetime(2023, 1, 1)
        self.reminder.set_reminder_date(valid_reminder_date)
        self.assertEqual(self.reminder.reminder_date, valid_reminder_date)

    def test_set_reminder_date_not_datetime(self):
        # Test setting a reminder date that is not a datetime
        with self.assertRaises(TypeError):
            self.reminder.set_reminder_date(123)

    def test_set_reminder_date_none(self):
        # Test setting a reminder date that is None
        with self.assertRaises(ValueError):
            self.reminder.set_reminder_date(None)

    def test_set_title_valid(self):
        # Test setting a valid title
        valid_title = "Valid Title"
        self.reminder.set_title(valid_title)
        self.assertEqual(self.reminder.title, valid_title)

    def test_set_title_not_string(self):
        # Test setting a title that is not a string
        with self.assertRaises(TypeError):
            self.reminder.set_title(123)

    def test_set_title_none(self):
        # Test setting a title that is None
        with self.assertRaises(ValueError):
            self.reminder.set_title(None)

    def test_set_title_whitespace(self):
        # Test setting a title that contains only whitespace
        with self.assertRaises(ValueError):
            self.reminder.set_title("   ")

    def test_set_title_empty(self):
        # Test setting an empty title
        with self.assertRaises(ValueError):
            self.reminder.set_title("")

    def test_set_title_too_long(self):
        # Test setting a title that is too long
        with self.assertRaises(ValueError):
            self.reminder.set_title("a" * 51)
    
    def test_set_title_max_length(self):
        # Test setting a title that is exactly at the maximum length
        max_length_title = "a" * 50
        self.reminder.set_title(max_length_title)
        self.assertEqual(self.reminder.title, max_length_title)

    def test_set_description_valid(self):
        # Test setting a valid description
        valid_description = "Valid Description"
        self.reminder.set_description(valid_description)
        self.assertEqual(self.reminder.description, valid_description)

    def test_set_description_not_string(self):
        # Test setting a description that is not a string
        with self.assertRaises(TypeError):
            self.reminder.set_description(123)

    def test_set_description_none(self):
        # Test setting a description that is None
        self.reminder.set_description(None)
        self.assertEqual(self.reminder.description, None)

    def test_set_description_too_long(self):
        # Test setting a description that is too long
        with self.assertRaises(ValueError):
            self.reminder.set_description("a" * 501)

    def test_set_description_max_length(self):
        # Test setting a description that is exactly at the maximum length
        max_length_description = "a" * 500
        self.reminder.set_description(max_length_description)
        self.assertEqual(self.reminder.description, max_length_description)

    def test_to_dict(self):
        # Verify if the dictionary returned has the expected keys and values
        expected_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "reminder_date": self.reminder_date,
            "schedules": self.schedules,
            "type": self.type
        }
        self.assertDictEqual(self.reminder.to_dict(), expected_dict)

    def test_to_dict_empty(self):
        # Verify if the dictionary returned has the expected keys and values
        # when there are empty attributes
        empty_reminder = ReminderElement(self.id, self.title, self.reminder_date)
        expected_dict = {
            "id": self.id,
            "title": self.title,
            "description": None,
            "reminder_date": self.reminder_date,
            "schedules": [],
            "type": "reminder"
        }
        
        self.assertDictEqual(empty_reminder.to_dict(), expected_dict)


if __name__ == '__main__':
    unittest.main()