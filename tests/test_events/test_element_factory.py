import unittest
from datetime import datetime
from unittest.mock import MagicMock
from src.calendar_elements.element_factory import CalendarElementFactory
from src.calendar_elements.element_types import EventElement, TaskElement, ReminderElement

class TestElementFactory(unittest.TestCase):

    def setUp(self):
        # Initialize the factory object
        self.factory = CalendarElementFactory()

    def test_create_element_event(self):
        """Test the creation of an event."""
        # Create an event
        event = self.factory.create_element("event", "1", "Test Event", 
                                            schedules = ['schedule1','schedule2'],
                                            description="Test_description",
                                             start=datetime(2023, 1, 1), 
                                             end=datetime(2023, 1, 2))
        # Verify if the event was created correctly
        self.assertIsInstance(event, EventElement)

    def test_create_element_task(self):
        """Test the creation of a task."""
        # Create a task
        task = self.factory.create_element("task", "2", "Test Task", schedules = ['schedule1','schedule2'],
                                           description="Task description", state = 'incomplete',
                                           due_date=datetime(2023, 1, 1))
        # Verify if the task was created correctly
        self.assertIsInstance(task, TaskElement)

    def test_create_element_reminder(self):
        """Test the creation of a reminder."""
        # Create a reminder
        reminder = self.factory.create_element("reminder", "3", "Test Reminder", 
                    schedules = ['schedule1','schedule2'],
                    description="Reminder description", 
                    reminder_date=datetime(2023, 1, 1))
        # Verify if the reminder was created correctly
        self.assertIsInstance(reminder, ReminderElement)

    def test_create_element_invalid_type(self):
        """Test the creation of an element with an invalid type."""
        # Verify if an exception is raised when trying to create an element with an invalid type
        with self.assertRaises(ValueError):
            self.factory.create_element("invalid_type", "4", "Invalid type", schedules = ['schedule1','schedule2'], 
                                        start=datetime(2023, 1, 1), end=datetime(2023, 1, 2))
            
if __name__ == '__main__':
    unittest.main()
