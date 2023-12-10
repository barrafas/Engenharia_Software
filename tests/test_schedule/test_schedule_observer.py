"""
Testing the Observer pattern implementation in the ScheduleManagement and Schedule classes
"""
import unittest
from src.schedule.schedule_model import Schedule

class TestScheduleObserver(unittest.TestCase):
    def setUp(self):
        # Set up for the tests
        class MockObserver:
            def __init__(self):
                self.notifications = []

            def update(self, schedule): ...
        
        self.observer = MockObserver()

    def test_subject_start_with_no_observers(self):
        permissions = {
            'user1': "read"
        }
        schedule = Schedule('schedule_id', 'title', 'description', permissions)
        
        initial_observers_len = len(schedule.__observers)
        self.assertEqual(initial_observers_len, 0)

    def test_subject_add_observer(self):
        permissions = {
            'user1': "read"
        }
        schedule = Schedule('schedule_id', 'title', 'description', permissions)
        
        schedule.attach(self.observer)
        observers_len = len(schedule.__observers)
        self.assertEqual(observers_len, 1)

        