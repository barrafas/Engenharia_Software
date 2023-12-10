"""
Testing the Observer pattern implementation in the ScheduleManagement and Schedule classes
"""
import unittest
from src.schedule.schedule_model import Schedule
from src.schedule.schedule_management import ScheduleManagement
from unittest.mock import MagicMock

class TestScheduleObserver(unittest.TestCase):
    def setUp(self):
        # Set up for the tests
        class MockObserver:
            def __init__(self):
                self.notifications = []

            def update(self, schedule):
                self.notifications.append(schedule)
        
        self.observer = MockObserver()

        self.db_module = MagicMock()
        self.schedule_management = ScheduleManagement.get_instance(self.db_module)

    def test_subject_start_with_no_observers(self):
        permissions = {
            'user1': "read"
        }
        schedule = Schedule('schedule_id', 'title', 'description', permissions)
        
        initial_observers_len = len(schedule.observers)
        self.assertEqual(initial_observers_len, 0)

    def test_subject_add_observer(self):
        permissions = {
            'user1': "read"
        }
        schedule = Schedule('schedule_id', 'title', 'description', permissions)
        
        schedule.attach(self.observer)
        observers_len = len(schedule.observers)
        self.assertEqual(observers_len, 1)
    
    def test_subject_remove_observer(self):
        permissions = {
            'user1': "read"
        }
        schedule = Schedule('schedule_id', 'title', 'description', permissions)
        
        schedule.attach(self.observer)
        schedule.detach(self.observer)
        observers_len = len(schedule.observers)
        self.assertEqual(observers_len, 0)

    def test_observer_gets_notified_on_elements_set(self):
        permissions = {
            'user1': "read"
        }
        schedule = Schedule('schedule_id', 'title', 'description', permissions)

        schedule.attach(self.observer)
        schedule.elements = ['element1', 'element2']
        # verificando se o observer chamou o método update
        self.assertEqual(len(self.observer.notifications), 1)

    def test_observer_gets_notified_on_title_set(self):
        permissions = {
            'user1': "read"
        }
        schedule = Schedule('schedule_id', 'title', 'description', permissions)

        schedule.attach(self.observer)
        schedule.set_title('new title')
        # verificando se o observer chamou o método update
        self.assertEqual(len(self.observer.notifications), 1)

        