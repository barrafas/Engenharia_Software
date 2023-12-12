"""
Testing the Observer pattern implementation in the ScheduleManagement and 
Schedule classes
"""
from unittest.mock import MagicMock
import unittest

from src.schedule.schedule_management import ScheduleManagement
from src.schedule.schedule_model import Schedule

class TestScheduleObserver(unittest.TestCase):
    """
    Testing the Observer pattern implementation in the ScheduleManagement and 
    Schedule classes

    methods:
        setUp
        test_subject_start_with_no_observers
        test_subject_add_observer
        test_subject_remove_observer
        test_observer_gets_notified_on_elements_set
        test_observer_gets_notified_on_title_set
        test_observer_gets_notified_on_description_set
        test_update_schedule_gets_called_when_schedule_is_updated
    """
    def setUp(self):
        """
        setting up the tests
        """
        # Set up for the tests
        class MockObserver:
            def __init__(self):
                self.notifications = []

            def update(self, schedule):
                self.notifications.append(schedule)

        self.observer = MockObserver()

        self.db_module = MagicMock()
        self.schedule_management = ScheduleManagement.get_instance(
            self.db_module)
        self.schedule_management.update_schedule = MagicMock()

    def test_subject_start_with_no_observers(self):
        """
        testing if the observers list starts empty
        """
        permissions = {
            'user1': "read"
        }
        schedule = Schedule('schedule_id', 'title', 'description', permissions)

        initial_observers_len = len(schedule.observers)
        self.assertEqual(initial_observers_len, 0)

    def test_subject_add_observer(self):
        """
        testing if the observer is added to the observers list
        """
        permissions = {
            'user1': "read"
        }
        schedule = Schedule('schedule_id', 'title', 'description', permissions)

        schedule.attach(self.observer)
        observers_len = len(schedule.observers)
        self.assertEqual(observers_len, 1)

    def test_subject_remove_observer(self):
        """
        testing if the observer is removed from the observers list
        """
        permissions = {
            'user1': "read"
        }
        schedule = Schedule('schedule_id', 'title', 'description', permissions)

        schedule.attach(self.observer)
        schedule.detach(self.observer)
        observers_len = len(schedule.observers)
        self.assertEqual(observers_len, 0)

    def test_observer_gets_notified_on_elements_set(self):
        """
        testing if the observer gets notified when the elements are set
        """
        permissions = {
            'user1': "read"
        }
        schedule = Schedule('schedule_id', 'title', 'description', permissions)

        schedule.attach(self.observer)
        schedule.elements = ['element1', 'element2']
        # verificando se o observer chamou o método update
        self.assertEqual(len(self.observer.notifications), 1)

    def test_observer_gets_notified_on_title_set(self):
        """
        testing if the observer gets notified when the title is set
        """
        permissions = {
            'user1': "read"
        }
        schedule = Schedule('schedule_id', 'title', 'description', permissions)

        schedule.attach(self.observer)
        schedule.set_title('new title')
        # verificando se o observer chamou o método update
        self.assertEqual(len(self.observer.notifications), 1)

    def test_observer_gets_notified_on_description_set(self):
        """
        testing if the observer gets notified when the description is set
        """
        permissions = {
            'user1': "read"
        }
        schedule = Schedule('schedule_id', 'title', 'description', permissions)

        schedule.attach(self.observer)
        schedule.set_description('new description')
        # verificando se o observer chamou o método update
        self.assertEqual(len(self.observer.notifications), 1)

    def test_update_schedule_gets_called_when_schedule_is_updated(self):
        """
        testing if the update_schedule method is called when the schedule is updated
        """
        permissions = {
            'user1': "read"
        }
        schedule = Schedule('schedule_id', 'title', 'description', permissions)

        schedule.attach(self.schedule_management)
        schedule.set_description('Sample change')

        self.schedule_management.update_schedule.assert_called_once_with(
            schedule.id)
