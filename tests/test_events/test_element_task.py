"""Module to test the TaskElement class."""

import unittest
from datetime import datetime
from src.calendar_elements.element_types import TaskElement
from tests.test_events.mocks import ScheduleManagement

class TestTaskElement(unittest.TestCase):
    """Test the TaskElement class"""

    def setUp(self):
        self.id = "1"
        self.title = "Test Task"
        self.due_date = datetime(2023, 1, 1)
        self.description = "Description"
        self.state = 'incomplete'
        self.schedules = ['schedule_1', 'schedule_2']
        self.element_type = "task"
        self.task = TaskElement(self.id,
                                self.title,
                                self.due_date,
                                self.schedules,
                                self.description, 
                                self.state,
                                self.element_type)
        
        # Access private attributes for testing
        self.task._TaskElement__id = self.id
        self.task._TaskElement__element_type = self.element_type
        self.task._TaskElement__schedules = self.schedules

    def test_id_property(self):
        """Test the id property"""
        self.assertEqual(self.task.id, self.id)

    def test_type_property(self):
        """Test the schedules property"""
        self.assertEqual(self.task.type, self.element_type)

    def test_schedules_property(self):
        """Test the schedules property"""
        self.assertEqual(self.task.schedules, self.schedules)

    def test_get_display_interval(self):
        """
        Verify if the interval returned matches the one that was set in the 
        constructor
        """
        expected_interval = (datetime(2022, 12, 31, 23, 50), datetime(2023, 1, 1))
        self.assertEqual(self.task.get_display_interval(), expected_interval)

    def test_get_schedules(self):
        """
        Verify if the schedules returned match the ones that were set in
        the constructor
        """
        schedule_management = ScheduleManagement.get_instance()
        task = TaskElement(element_id=self.id, 
                            title=self.title, 
                            due_date=self.due_date, 
                            schedules=['id1', 'id2', 'id3'],
                            description=self.description)
        schedules = task.get_schedules()
        expected_schedule = [schedule_management.schedules[id] for id in ['id1', 'id2', 'id3']]
        self.assertEqual(schedules, expected_schedule)

    def test_get_users(self):
        """
        Test if the users returned match the ones that were set in the 
        constructor
        """

    def test_get_users_empty(self):
        """Test if an empty list is returned when there are no users"""

    def test_get_users_with_filter_by_schedules(self):
        """
        Test if the users returned match the ones that were set in the 
        constructor and if they belong to the specified schedules
        """

    def test_set_due_date_valid(self):
        """Test setting a valid due date"""
        valid_due_date = datetime(2023, 1, 1)
        self.task.set_due_date(valid_due_date)
        self.assertEqual(self.task.due_date, valid_due_date)

    def test_set_due_date_not_datetime(self):
        """Test setting a due date that is not a datetime"""
        with self.assertRaises(TypeError):
            self.task.set_due_date(123)

    def test_set_due_date_none(self):
        """Test setting a due date that is None"""
        with self.assertRaises(ValueError):
            self.task.set_due_date(None)

    def test_set_state(self):
        """Verify if the state is set correctly"""
        states = ['incomplete', 'complete', 'cancelled']
        for state in states:
            self.task.set_state(state)
            self.assertEqual(self.task.state, state)

    def test_set_state_none(self):
        """Verify if a None state set the state as incomplete"""
        self.task.set_state(None)
        self.assertEqual(self.task.state, 'incomplete')

    def test_set_state_invalid(self):
        """Verify if an invalid state raises a ValueError"""
        with self.assertRaises(ValueError):
            self.task.set_state("invalid")

    def test_set_state_not_string(self):
        """Verify if a non-string state raises a TypeError"""
        with self.assertRaises(TypeError):
            self.task.set_state(123)

    def test_set_title_valid(self):
        """Test setting a valid title"""
        valid_title = "Valid Title"
        self.task.set_title(valid_title)
        self.assertEqual(self.task.title, valid_title)

    def test_set_title_not_string(self):
        """Test setting a title that is not a string"""
        with self.assertRaises(TypeError):
            self.task.set_title(123)

    def test_set_title_none(self):
        """Test setting a title that is None"""
        with self.assertRaises(ValueError):
            self.task.set_title(None)

    def test_set_title_whitespace(self):
        """Test setting a title that contains only whitespace"""
        with self.assertRaises(ValueError):
            self.task.set_title("   ")

    def test_set_title_empty(self):
        """Test setting an empty title"""
        with self.assertRaises(ValueError):
            self.task.set_title("")

    def test_set_title_too_long(self):
        """Test setting a title that is too long"""
        with self.assertRaises(ValueError):
            self.task.set_title("a" * 51)
    
    def test_set_title_max_length(self):
        """Test setting a title that is exactly at the maximum length"""
        max_length_title = "a" * 50
        self.task.set_title(max_length_title)
        self.assertEqual(self.task.title, max_length_title)

    def test_set_description_valid(self):
        """Test setting a valid description"""
        valid_description = "Valid Description"
        self.task.set_description(valid_description)
        self.assertEqual(self.task.description, valid_description)

    def test_set_description_not_string(self):
        """Test setting a description that is not a string"""
        with self.assertRaises(TypeError):
            self.task.set_description(123)

    def test_set_description_none(self):
        """Test setting a description that is None"""
        self.task.set_description(None)
        self.assertEqual(self.task.description, None)

    def test_set_description_too_long(self):
        """Test setting a description that is too long"""
        with self.assertRaises(ValueError):
            self.task.set_description("a" * 501)

    def test_set_description_max_length(self):
        """Test setting a description that is exactly at the maximum length"""
        max_length_description = "a" * 500
        self.task.set_description(max_length_description)
        self.assertEqual(self.task.description, max_length_description)

    def test_to_dict(self):
        """Verify if the dictionary returned has the expected keys and values"""
        expected_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "state": self.state,
            "schedules": self.schedules,
            "element_type": self.element_type
        }
        self.assertDictEqual(self.task.to_dict(), expected_dict)

if __name__ == '__main__':
    unittest.main()
