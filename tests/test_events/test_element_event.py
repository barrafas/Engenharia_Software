"""Module to test the EventElement class"""

import unittest
from datetime import datetime
from src.calendar_elements.element_types import EventElement, ScheduleManagement, Schedule, UserManagement
from unittest.mock import MagicMock, PropertyMock
from src.user.user_model import User


class TestEventElement(unittest.TestCase):
    """Test the EventElement class"""

    def setUp(self):
        self.id = "1"
        self.title = "Test Event"
        self.start = datetime(2023, 1, 1)
        self.end = datetime(2023, 1, 2)
        self.description = "Description"
        self.schedules = ['schedule_1', 'schedule_2']
        self.element_type = "event"
        self.event = EventElement(self.id,
                                    self.title,
                                    self.start,
                                    self.end,
                                    self.schedules,
                                    self.description)
        # Access private attributes for testing
        self.event._EventElement__id = self.id
        self.event._EventElement__schedules = self.schedules
        self.event._EventElement__element_type = self.element_type
        
    def test_id_property(self):
        """Test the id property"""
        self.assertEqual(self.event.id, self.id)

    def test_type_property(self):
        """Test the schedules property"""
        self.assertEqual(self.event.type, self.element_type)

    def test_schedules_property(self):
        """Test the schedules property"""
        self.assertEqual(self.event.schedules, self.schedules)

    def test_get_display_interval(self):
        """
        Test if the interval returned matches the one that was set in the
        constructor
        """
        expected_interval = (datetime(2023, 1, 1), datetime(2023, 1, 2))
        self.assertEqual(self.event.get_display_interval(), expected_interval)

    def test_get_schedules(self):
        """
        Test if the schedules returned match the ones that were set in the
        constructor
        """
        schedule_1 = MagicMock(spec=Schedule)
        type(schedule_1).id = PropertyMock(return_value='schedule_1')

        schedule_2 = MagicMock(spec=Schedule)
        type(schedule_2).id = PropertyMock(return_value='schedule_2')

        def get_schedule_mock(id: str) -> Schedule:
            return {
                'schedule_1': schedule_1,
                'schedule_2': schedule_2
            }.get(id, None)

        with unittest.mock.patch.object(ScheduleManagement, 'get_schedule', side_effect=get_schedule_mock):
            schedules = self.event.get_schedules()
            self.assertEqual(schedules, [schedule_1, schedule_2])

    def test_get_users(self):
        """
        Test if the users returned match the ones that were set in the 
        constructor
        """
         # Set up the mock objects
        schedule_1 = MagicMock(spec=Schedule)
        type(schedule_1).id = PropertyMock(return_value='schedule_1')
        type(schedule_1).permissions = PropertyMock(return_value={"user_1": "owner", "user_2": "editor"})

        schedule_2 = MagicMock(spec=Schedule)
        type(schedule_2).id = PropertyMock(return_value='schedule_2')
        type(schedule_2).permissions = PropertyMock(return_value={"user_3": "owner", "user_4": "editor"})

        user_1 = MagicMock(spec=User)
        type(user_1).id = PropertyMock(return_value='user_1')
        type(user_1).username = PropertyMock(return_value='user_1')
        user_2 = MagicMock(spec=User)
        type(user_2).id = PropertyMock(return_value='user_2')
        type(user_2).username = PropertyMock(return_value='user_2')
        user_3 = MagicMock(spec=User)
        type(user_3).id = PropertyMock(return_value='user_3')
        type(user_3).username = PropertyMock(return_value='user_3')
        user_4 = MagicMock(spec=User)
        type(user_4).id = PropertyMock(return_value='user_4')
        type(user_4).username = PropertyMock(return_value='user_4')

        def get_user_mock(id: str) -> User:
            return {
                'user_1': user_1,
                'user_2': user_2,
                'user_3': user_3,
                'user_4': user_4
            }.get(id, None)

        def get_schedule_mock(id: str) -> Schedule:
            return {
                'schedule_1': schedule_1,
                'schedule_2': schedule_2
            }.get(id, None)
        
        with unittest.mock.patch.object(ScheduleManagement, 'get_schedule', side_effect=get_schedule_mock):
            with unittest.mock.patch.object(UserManagement, 'get_user', side_effect=get_user_mock):
                users = self.event.get_users(['schedule_1', 'schedule_2'])
                self.assertEqual(len(users), 4)
                for user in users:
                    self.assertIn(user, [user_1, user_2, user_3, user_4])

    def test_get_users_with_filter_by_schedules(self):
        """
        Test if the users returned match the ones that were set in the 
        constructor and if they belong to the specified schedules
        """

    def test_set_interval_valid(self):
        """Test setting a valid interval"""
        valid_start = datetime(2023, 1, 1)
        valid_end = datetime(2023, 1, 2)
        self.event.set_interval(valid_start, valid_end)
        self.assertEqual(self.event.start, valid_start)
        self.assertEqual(self.event.end, valid_end)

    def test_set_interval_not_datetime(self):
        """Test setting an interval that is not a datetime"""
        with self.assertRaises(TypeError):
            self.event.set_interval(123, 456)

    def test_set_interval_start_after_end(self):
        """Test setting an interval where the start is after the end"""
        with self.assertRaises(ValueError):
            self.event.set_interval(self.end, self.start)

    def test_set_interval_start_none(self):
        """Test setting an interval where the start is None"""
        with self.assertRaises(ValueError):
            self.event.set_interval(None, self.end)

    def test_set_interval_end_none(self):
        """Test setting an interval where the end is None"""
        with self.assertRaises(ValueError):
            self.event.set_interval(self.start, None)

    def test_set_title_valid(self):
        """Test setting a valid title"""
        valid_title = "Valid Title"
        self.event.set_title(valid_title)
        self.assertEqual(self.event.title, valid_title)

    def test_set_title_not_string(self):
        """Test setting a title that is not a string"""
        with self.assertRaises(TypeError):
            self.event.set_title(123)

    def test_set_title_none(self):
        """Test setting a title that is None"""
        with self.assertRaises(ValueError):
            self.event.set_title(None)

    def test_set_title_whitespace(self):
        """Test setting a title that contains only whitespace"""
        with self.assertRaises(ValueError):
            self.event.set_title("   ")

    def test_set_title_empty(self):
        """Test setting an empty title"""
        with self.assertRaises(ValueError):
            self.event.set_title("")

    def test_set_title_too_long(self):
        """Test setting a title that is too long"""
        with self.assertRaises(ValueError):
            self.event.set_title("a" * 51)
    
    def test_set_title_max_length(self):
        """Test setting a title that is exactly at the maximum length"""
        max_length_title = "a" * 50
        self.event.set_title(max_length_title)
        self.assertEqual(self.event.title, max_length_title)

    def test_set_description_valid(self):
        """Test setting a valid description"""
        valid_description = "Valid Description"
        self.event.set_description(valid_description)
        self.assertEqual(self.event.description, valid_description)

    def test_set_description_not_string(self):
        """Test setting a description that is not a string"""
        with self.assertRaises(TypeError):
            self.event.set_description(123)

    def test_set_description_none(self):
        """Test setting a description that is None"""
        self.event.set_description(None)
        self.assertEqual(self.event.description, None)

    def test_set_description_too_long(self):
        """Test setting a description that is too long"""
        with self.assertRaises(ValueError):
            self.event.set_description("a" * 501)

    def test_set_description_max_length(self):
        """Test setting a description that is exactly at the maximum length"""
        max_length_description = "a" * 500
        self.event.set_description(max_length_description)
        self.assertEqual(self.event.description, max_length_description)

    def test_to_dict(self):
        """Verify if the dictionary returned has the expected keys and values"""
        expected_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "element_type": self.element_type,
            "schedules": self.schedules,
            "start": self.start,
            "end": self.end
        }
        self.assertDictEqual(self.event.to_dict(), expected_dict)


if __name__ == '__main__':
    unittest.main()
