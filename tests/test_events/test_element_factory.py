import unittest
from datetime import datetime
from unittest.mock import MagicMock
from src.calendar_elements.element_factory import CalendarElementFactory
from src.calendar_elements.element_types import EventElement, TaskElement, ReminderElement

class TestElementFactory(unittest.TestCase):
    """Test the CalendarElementFactory class"""

    def setUp(self):
        # Initialize the factory object
        self.factory = CalendarElementFactory()

    def test_create_element_event(self):
        """Test the creation of an event."""
        # Create an event
        event = self.factory.create_element(element_type = "event",
                                            element_id = "1",
                                            title = "Test Event",
                                            schedules = ['schedule1','schedule2'],
                                            description="Test_description",
                                            start=datetime(2023, 1, 1),
                                            end=datetime(2023, 1, 2))
        # Verify if the event was created correctly
        self.assertIsInstance(event, EventElement)

    def test_create_element_task(self):
        """Test the creation of a task."""
        # Create a task
        task = self.factory.create_element(element_type = "task",
                                            element_id = "2",
                                            title = "Test Task",
                                            schedules = ['schedule1','schedule2'],
                                            description="Task description",
                                            state = 'incomplete',
                                            due_date=datetime(2023, 1, 1))
        # Verify if the task was created correctly
        self.assertIsInstance(task, TaskElement)

    def test_create_element_reminder(self):
        """Test the creation of a reminder."""
        # Create a reminder
        reminder = self.factory.create_element(element_type = "reminder",
                                                element_id = "3",
                                                title = "Test Reminder",
                                                schedules = ['schedule1','schedule2'],
                                                description="Reminder description",
                                                reminder_date=datetime(2023, 1, 1))
        # Verify if the reminder was created correctly
        self.assertIsInstance(reminder, ReminderElement)

    def test_create_element_invalid_type(self):
        """Test the creation of an element with an invalid type."""
        # Verify if an exception is raised when trying to create an element with an invalid type
        with self.assertRaises(ValueError):
            self.factory.create_element(element_type = "invalid_type",
                                        element_id = "4",
                                        title = "Invalid type",
                                        schedules = ['schedule1','schedule2'],
                                        start=datetime(2023, 1, 1),
                                        end=datetime(2023, 1, 2))

if __name__ == '__main__':
    unittest.main()
