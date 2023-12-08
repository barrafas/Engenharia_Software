import unittest
from datetime import datetime, timedelta
from src.calendar_elements.element_types import EventElement, TaskElement, ReminderElement

class TestEventElement(unittest.TestCase):

    def setUp(self):
        self.event = EventElement("1", "Test Event", "event_description", datetime(2023, 1, 1), 
                                  datetime(2023, 1, 2))
        
    def test_get_display_interval(self):
        # Verify if the interval returned matches the one that was set in 
        # the constructor
        expected_interval = (datetime(2023, 1, 1), datetime(2023, 1, 2))
        self.assertEqual(self.event.get_display_interval(), expected_interval)

    def test_get_type(self):
        # Verify if the type returned is "evento"
        self.assertEqual(self.event.get_type(), "evento")

    def test_get_schedules(self):
        pass

    def test_get_users(self):    
        pass

    def test_set_title_valid(self):
        # Test setting a valid title
        valid_title = "Valid Title"
        self.event.set_title(valid_title)
        self.assertEqual(self.event.title, valid_title)

    def test_set_title_not_string(self):
        # Test setting a title that is not a string
        with self.assertRaises(TypeError):
            self.event.set_title(123)

    def test_set_title_none(self):
        # Test setting a title that is None
        with self.assertRaises(ValueError):
            self.event.set_title(None)

    def test_set_title_whitespace(self):
        # Test setting a title that contains only whitespace
        with self.assertRaises(ValueError):
            self.event.set_title("   ")

    def test_set_title_empty(self):
        # Test setting an empty title
        with self.assertRaises(ValueError):
            self.event.set_title("")

    def test_set_title_too_long(self):
        # Test setting a title that is too long
        with self.assertRaises(ValueError):
            self.event.set_title("a" * 51)
    
    def test_set_title_max_length(self):
        # Test setting a title that is exactly at the maximum length
        max_length_title = "a" * 50
        self.event.set_title(max_length_title)
        self.assertEqual(self.event.title, max_length_title)

    def test_set_description_valid(self):
        # Test setting a valid description
        valid_description = "Valid Description"
        self.event.set_description(valid_description)
        self.assertEqual(self.event.description, valid_description)

    def test_set_description_not_string(self):
        # Test setting a description that is not a string
        with self.assertRaises(TypeError):
            self.event.set_description(123)

    def test_set_description_none(self):
        # Test setting a description that is None
        self.event.set_description(None)
        self.assertEqual(self.event.description, None)

    def test_set_description_too_long(self):
        # Test setting a description that is too long
        with self.assertRaises(ValueError):
            self.event.set_description("a" * 501)

    def test_set_description_max_length(self):
        # Test setting a description that is exactly at the maximum length
        max_length_description = "a" * 500
        self.event.set_description(max_length_description)
        self.assertEqual(self.event.description, max_length_description)

    def test_to_dict(self):
        # Verify if the dictionary returned has the expected keys and values
        expected_dict = {
            "id": "1",
            "title": "Test Event",
            "description": "Description",
            "start": datetime(2023, 1, 1),
            "end": datetime(2023, 1, 2),
            "type": "evento",
            "schedules": []
        }
        self.assertDictEqual(self.event.to_dict(), expected_dict)

    

class TestTaskElement(unittest.TestCase):

    def setUp(self):
        self.task = TaskElement("1", "Test Task", "Description", 
                                datetime(2023, 1, 1))

    def test_get_display_interval(self):
        # Verify if the interval returned matches the one that was set in the 
        # constructor
        expected_interval = (
            datetime(2022, 12, 31, 23, 50), datetime(2023, 1, 1))
        self.assertEqual(self.task.get_display_interval(), expected_interval)

    def test_get_type(self):
        # Verify if the type returned is "tarefa"
        self.assertEqual(self.task.get_type(), "tarefa")

    def test_get_title(self):
        # Verify if the title returned is the same that was set in the 
        # constructor
        self.assertEqual(self.task.get_title(), "Test Task")

    def test_to_dict(self):
        # Verify if the dictionary returned has the expected keys and values
        expected_dict = {
            "id": "1",
            "title": "Test Task",
            "description": "Description",
            "state": "incompleta",
            "due_date": datetime(2023, 1, 1),
            "type": "tarefa",
            "schedules": []
        }
        self.assertDictEqual(self.task.to_dict(), expected_dict)

    def test_set_state(self):
        # Verify if the state is set correctly
        self.task.set_state("completa")
        self.assertEqual(self.task.state, "completa")
        pass

    def test_get_users(self):
        pass

class TestReminderElement(unittest.TestCase):

    def setUp(self):
        self.reminder = ReminderElement("1", "Test Reminder", "Description", 
                                        datetime(2023, 1, 1))

    def test_get_display_interval(self):
        # Verify if the interval returned matches the one that was set in 
        # the constructor
        expected_interval = (
            datetime(2022, 12, 31, 23, 50), datetime(2023, 1, 1))
        self.assertEqual(self.reminder.get_display_interval(), expected_interval)

    def test_get_type(self):
        # Verify if the type returned is "lembrete"
        self.assertEqual(self.reminder.get_type(), "lembrete")

    def test_to_dict(self):
        # Verify if the dictionary returned has the expected keys and values
        expected_dict = {
            "id": "1",
            "title": "Test Reminder",
            "description": "Description",
            "reminder_date": datetime(2023, 1, 1),
            "type": "lembrete",
            "schedules": []
        }
        self.assertDictEqual(self.reminder.to_dict(), expected_dict)

    def test_get_users(self):
        pass

if __name__ == '__main__':
    unittest.main()
