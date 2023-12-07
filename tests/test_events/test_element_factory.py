import unittest
from datetime import datetime
from unittest.mock import MagicMock
from src.calendar_elements.element_factory import CalendarElementFactory, EventAlreadyExistsError, EventDoesNotExistError
from src.calendar_elements.element_types import EventElement, TaskElement, ReminderElement

class TestElementFactory(unittest.TestCase):

    def setUp(self):
        # Initialize the factory object
        self.factory = CalendarElementFactory()

    def test_create_element_event(self):
        """Test the creation of an event."""
        # Create an event
        event = self.factory.create_element("evento", "1", "Test Event", start=datetime(2023, 1, 1), end=datetime(2023, 1, 2))
        # Verify if the event was created correctly
        self.assertIsInstance(event, EventElement)

    def test_create_element_task(self):
        """Test the creation of a task."""
        # Create a task
        task = self.factory.create_element("tarefa", "2", "Test Task", description="Task description", due_date=datetime(2023, 1, 1))
        # Verify if the task was created correctly
        self.assertIsInstance(task, TaskElement)

    def test_create_element_reminder(self):
        """Test the creation of a reminder."""
        # Create a reminder
        reminder = self.factory.create_element("lembrete", "3", "Test Reminder", description="Reminder description", reminder_date=datetime(2023, 1, 1))
        # Verify if the reminder was created correctly
        self.assertIsInstance(reminder, ReminderElement)

    def test_create_element_invalid_type(self):
        """Test the creation of an element with an invalid type."""
        # Verify if an exception is raised when trying to create an element with an invalid type
        with self.assertRaises(ValueError):
            self.factory.create_element("invalid_type", "4", "Invalid Element", start=datetime(2023, 1, 1), end=datetime(2023, 1, 2))


if __name__ == '__main__':
    unittest.main()
