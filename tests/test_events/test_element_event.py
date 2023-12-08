import unittest
from datetime import datetime, timedelta
from src.calendar_elements.element_types import EventElement
from tests.test_events.mocks import Schedule, ScheduleManagement, User, UserManagement

class TestEventElement(unittest.TestCase):

    def setUp(self):
        self.id = "1"
        self.title = "Test Event"
        self.start = datetime(2023, 1, 1)
        self.end = datetime(2023, 1, 2)
        self.description = "Description"
        self.schedules = ['schedule1', 'schedule2']
        self.type = "event"
        self.event = EventElement(self.id, self.title, self.start, self.end, 
                                    self.description, self.schedules)
        # Access private attributes for testing
        self.event._EventElement__id = self.id
        self.event._EventElement__schedules = self.schedules
        self.event._EventElement__type = self.type
        
    def test_id_property(self):
        # Test the id property
        self.assertEqual(self.event.id, self.id)

    def test_type_property(self):
        # Test the schedules property
        self.assertEqual(self.event.type, self.type)

    def test_schedules_property(self):
        # Test the schedules property
        self.assertEqual(self.event.schedules, self.schedules)

    def test_get_display_interval(self):
        # Verify if the interval returned matches the one that was set in 
        # the constructor
        expected_interval = (datetime(2023, 1, 1), datetime(2023, 1, 2))
        self.assertEqual(self.event.get_display_interval(), expected_interval)

    def test_get_type(self):
        # Verify if the type returned is "event"
        self.assertEqual(self.event.get_type(), "event")

    def test_get_schedules(self):
        # Verify if the schedules returned match the ones that were set in 
        # the constructor
        schedule_management = ScheduleManagement.get_instance()
        event = EventElement(self.id, self.title, self.start, self.end, self.description, 
                             ['id1', 'id2', 'id3'])
        schedules = event.get_schedules()
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

    def test_set_interval_valid(self):
        # Test setting a valid interval
        valid_start = datetime(2023, 1, 1)
        valid_end = datetime(2023, 1, 2)
        self.event.set_interval(valid_start, valid_end)
        self.assertEqual(self.event.start, valid_start)
        self.assertEqual(self.event.end, valid_end)

    def test_set_interval_not_datetime(self):
        # Test setting an interval that is not a datetime
        with self.assertRaises(TypeError):
            self.event.set_interval(123, 456)

    def test_set_interval_start_after_end(self):
        # Test setting an interval where the start is after the end
        with self.assertRaises(ValueError):
            self.event.set_interval(self.end, self.start)

    def test_set_interval_start_none(self):
        # Test setting an interval where the start is None
        with self.assertRaises(ValueError):
            self.event.set_interval(None, self.end)

    def test_set_interval_end_none(self):
        # Test setting an interval where the end is None
        with self.assertRaises(ValueError):
            self.event.set_interval(self.start, None)

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
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "type": self.type,
            "schedules": self.schedules,
            "start": self.start,
            "end": self.end
        }
        self.assertDictEqual(self.event.to_dict(), expected_dict)


    def test_to_dict_empty_kwargs(self):
        # Verify if the dictionary returned has the expected keys and values
        # when the event is instantiated with empty kwargs
        empty_event = EventElement(self.id, self.title, self.start, self.end)
        expected_dict = {
            "id": self.id,
            "title": self.title,
            "start": self.start,
            "end": self.end,
            "description": None,
            "type": 'event',
            "schedules": []
        }
        self.assertDictEqual(empty_event.to_dict(), expected_dict)

if __name__ == '__main__':
    unittest.main()