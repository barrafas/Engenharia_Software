"""Module to test the EventElement class"""

from unittest.mock import MagicMock, PropertyMock
from datetime import datetime
from typing import Optional
import unittest

from src.calendar_elements.element_management import ElementManagement
from src.schedule.schedule_management import ScheduleManagement
from src.calendar_elements.element_types import EventElement
from src.user.user_management import UserManagement
from src.schedule.schedule_model import Schedule
from src.user.user_model import User


class TestEventElement(unittest.TestCase):
    """Test the EventElement class"""

    def setUp(self):
        """Function that runs before each test case"""
        db_module_mock = MagicMock()

        # initialize the Managements
        ScheduleManagement.get_instance(db_module_mock)
        UserManagement.get_instance(db_module_mock)

        self.id = "1"
        self.title = "Test Event"
        self.start = datetime(2023, 1, 1)
        self.end = datetime(2023, 1, 2)
        self.description = "Description"
        self.schedules = ["schedule_1", "schedule_2"]
        self.element_type = "event"
        self.event = EventElement(
            self.id, self.title, self.start, self.end, self.schedules, self.description
        )
        # Access private attributes for testing
        self.event._EventElement__id = self.id
        self.event._EventElement__schedules = self.schedules
        self.event._EventElement__element_type = self.element_type

    def test_id_property(self):
        """Test the id property"""
        self.assertEqual(self.event.id, self.id)

    def test_type_property(self):
        """Test the schedules property"""
        self.assertEqual(self.event.element_type, self.element_type)

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
        # Set up the mock objects and functions
        get_schedule_mock, schedule_1, schedule_2 = self.get_mock_schedule()

        with unittest.mock.patch.object(
            ScheduleManagement, "get_schedule", side_effect=get_schedule_mock
        ):
            schedules = self.event.get_schedules()
            self.assertEqual(schedules, [schedule_1, schedule_2])

    def test_get_users(self):
        """
        Test if the users returned match the ones that were set in the
        constructor
        """
        # Set up the mock objects and functions
        get_schedule_mock, _, _ = self.get_mock_schedule()
        get_user_mock, user_1, user_2, user_3, user_4 = self.get_mock_user()

        with unittest.mock.patch.object(
            ScheduleManagement, "get_schedule", side_effect=get_schedule_mock
        ):
            with unittest.mock.patch.object(
                UserManagement, "get_user", side_effect=get_user_mock
            ):
                users = self.event.get_users(["schedule_1", "schedule_2"])
                self.assertEqual(len(users), 4)
                for user in users:
                    self.assertIn(user, [user_1, user_2, user_3, user_4])

    def test_get_users_nonfilter(self):
        """Test get_users when no filter of schedules are not specified.
        Default to all schedules.
        #"""
        # Set up the mock objects and functions
        get_schedule_mock, _, _ = self.get_mock_schedule()
        get_user_mock, user_1, user_2, user_3, user_4 = self.get_mock_user()

        with unittest.mock.patch.object(
            ScheduleManagement, "get_schedule", side_effect=get_schedule_mock
        ):
            with unittest.mock.patch.object(
                UserManagement, "get_user", side_effect=get_user_mock
            ):
                users = self.event.get_users()
                self.assertEqual(len(users), 4)
                for user in users:
                    self.assertIn(user, [user_1, user_2, user_3, user_4])

    def test_get_users_with_filter_by_schedules(self):
        """
        Test if the users returned match the ones that were set in the
        constructor and if they belong to the specified schedules
        """
        # Set up the mock objects
        get_schedule_mock, _, _ = self.get_mock_schedule()
        get_user_mock, user_1, user_2, user_3, user_4 = self.get_mock_user()

        with unittest.mock.patch.object(
            ScheduleManagement, "get_schedule", side_effect=get_schedule_mock
        ):
            with unittest.mock.patch.object(
                UserManagement, "get_user", side_effect=get_user_mock
            ):
                users = self.event.get_users(["schedule_1"])
                self.assertEqual(len(users), 2)
                for user in users:
                    self.assertIn(user, [user_1, user_2, user_3, user_4])

    def test_get_users_nonrepeat_users(self):
        """Test if the users returned are unique"""
        # Set up the mock objects
        get_schedule_mock, _, _ = self.get_mock_schedule(
            repeat_user=True
        )
        get_user_mock, user_1, user_2, _, _ = self.get_mock_user()

        with unittest.mock.patch.object(
            ScheduleManagement, "get_schedule", side_effect=get_schedule_mock
        ):
            with unittest.mock.patch.object(
                UserManagement, "get_user", side_effect=get_user_mock
            ):
                users = self.event.get_users(["schedule_1", "schedule_2"])
                self.assertEqual(len(users), 2)
                for user in users:
                    self.assertIn(user, [user_1, user_2])

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
            "_id": self.id,
            "title": self.title,
            "description": self.description,
            "element_type": self.element_type,
            "schedules": self.schedules,
            "start": self.start,
            "end": self.end,
        }
        self.assertDictEqual(self.event.to_dict(), expected_dict)

    def test_changes_on_elements_calls_element_management_update_element(self):
        """
        Verify if the update_element method is called when the
        elements are changed.
        """
        element = EventElement(
            "event1",
            "title1",
            datetime(2021, 1, 1),
            datetime(2021, 1, 2),
            ["schedule1"],
            "description1",
        )
        element_management = ElementManagement.get_instance(database_module=MagicMock())
        element_management.update_element = MagicMock()
        element.attach(element_management)
        # Act
        element.schedules = ["schedule2"]
        # Assert
        element_management.update_element.assert_called_once_with("event1")

    def get_mock_schedule(self,
                        repeat_user=False
                        ) -> tuple[callable, MagicMock, MagicMock]:
        """Mock function to return a schedule object"""

        # Set up the mock objects
        schedule_1 = MagicMock(spec=Schedule)
        type(schedule_1).id = PropertyMock(return_value="schedule_1")
        type(schedule_1).permissions = PropertyMock(
            return_value={"user_1": "owner", "user_2": "editor"}
        )

        schedule_2 = MagicMock(spec=Schedule)
        type(schedule_2).id = PropertyMock(return_value="schedule_2")
        if repeat_user:
            type(schedule_2).permissions = PropertyMock(
                return_value={"user_1": "owner", "user_2": "editor"}
            )
        else:
            type(schedule_2).permissions = PropertyMock(
                return_value={"user_3": "owner", "user_4": "editor"}
            )

        def get_schedule_mock(id: str) -> Optional[MagicMock]:
            return {"schedule_1": schedule_1, "schedule_2": schedule_2}.get(id, None)

        return get_schedule_mock, schedule_1, schedule_2

    def get_mock_user(self) -> tuple[callable, MagicMock, MagicMock, MagicMock, MagicMock]:
        """Mock function to return a user object"""

        # Set up the mock objects
        user_1 = MagicMock(spec=User)
        type(user_1).id = PropertyMock(return_value="user_1")
        type(user_1).username = PropertyMock(return_value="user_1")

        user_2 = MagicMock(spec=User)
        type(user_2).id = PropertyMock(return_value="user_2")
        type(user_2).username = PropertyMock(return_value="user_2")

        user_3 = MagicMock(spec=User)
        type(user_3).id = PropertyMock(return_value="user_3")
        type(user_3).username = PropertyMock(return_value="user_3")

        user_4 = MagicMock(spec=User)
        type(user_4).id = PropertyMock(return_value="user_4")
        type(user_4).username = PropertyMock(return_value="user_4")

        def get_user_mock(id: str) -> Optional[MagicMock]:
            return {
                "user_1": user_1,
                "user_2": user_2,
                "user_3": user_3,
                "user_4": user_4,
            }.get(id, None)

        return get_user_mock, user_1, user_2, user_3, user_4


if __name__ == "__main__": # pragma: no cover
    unittest.main() # pragma: no cover
