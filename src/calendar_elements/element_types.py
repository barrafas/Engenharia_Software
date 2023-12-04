"""
    This module contains the classes that represent the different types of
    elements that can be displayed in the calendar.
"""
from datetime import datetime
from .element_interface import CalendarElement


class EventElement(CalendarElement):
    """
        A class that represents an event.

        'Event with determined beginning and end dates, which can be
        scheduled for a specific time, and which can be
        assigned to one or more schedules.'
    """

    def __init__(self, element_id: str, title: str, start: datetime, end: datetime):
        """
        EventElement constructor.

        Arguments:
            element_id -- The id of the event.
            title -- The title of the event.
            start -- The start date of the event.
            end -- The end date of the event.
        """
        self._id = element_id
        self.title = title
        self.start = start
        self.end = end
        self._schedules = []
        self._type = "evento"

    def get_display_interval(self) -> (datetime, datetime):
        """
        Returns the interval that the event should ocupate in the calendar.

        Returns:
            (datetime, datetime) -- The interval that the event should ocupate in the calendar.
        """
        return (self.start, self.end)

    def get_type(self) -> str:
        """
        Returns the type of the event.

        Returns:
            str -- The type of the event.
        """
        return self._type

    def get_title(self) -> str:
        """
        Returns the title of the event.

        Returns:
            str -- The title of the event.
        """
        return self.title

    def get_users(self) -> [str]:
        """
        Returns the users that are assigned to the event.

        Returns:
            [str] -- The users that are assigned to the event.
        """

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the event.

        Returns:
            dict -- The dictionary representation of the event.
        """
        return {
            "id": self._id,
            "title": self.title,
            "start": self.start,
            "end": self.end,
            "type": self._type,
            "schedules": self._schedules
        }


class TaskElement(CalendarElement):
    """
        A class that represents a task.

        'Task with a deadline, which can be scheduled for a specific
        time, and which can be assigned to one or more schedules.'
    """

    def __init__(self, element_id: str, title: str, description: str, due_date: datetime):
        """
        TaskElement constructor.

        Arguments:
            element_id -- The id of the task.
            title -- The title of the task.
            description -- The description of the task.
            due_date -- The due date of the task.
        """
        self._id = element_id
        self.title = title
        self.description = description
        self.state = "incompleta"
        self.due_date = due_date
        self._schedules = []
        self._type = "tarefa"

    def get_display_interval(self) -> (datetime, datetime):
        """
        Returns the interval that the task should ocupate in the calendar.
        In the case of the task, it will be 10 minutes before
        the due date untill the due date.
        Returns:
            (datetime, datetime) -- The interval that the task should ocupate in the calendar.
        """
        ending_date = self.due_date
        # The task will be displayed 10 minutes before the due date.
        starting_date = ending_date.replace(
            minute=ending_date.minute - 10)
        return (starting_date, ending_date)

    def get_type(self) -> str:
        """
        Returns the type of the task.

        Returns:
            str -- The type of the task.
        """
        return self._type

    def get_title(self) -> str:
        """
        Returns the title of the task.

        Returns:
            str -- The title of the task.
        """
        return self.title

    def get_schedules(self) -> list:
        """
        Returns the schedules of the task.

        Returns:
            list -- The schedules of the task.
        """
        return self._schedules

    def get_users(self) -> list:
        """
        Returns the users assigned to the task.

        Returns:
            list -- The users assigned to the task.
        """

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the task.

        Returns:
            dict -- The dictionary representation of the task.
        """
        return {
            "id": self._id,
            "title": self.title,
            "description": self.description,
            "state": self.state,
            "due_date": self.due_date,
            "type": self._type,
            "schedules": self._schedules
        }

    def set_state(self, state: str):
        """
        Sets the state of the task.

        Arguments:
            state -- The new state of the task.
        """
        self.state = state


class ReminderElement(CalendarElement):
    """
        A class that represents a reminder.

        'Reminder with a date and time, which can be scheduled for a specific
        time, and which can be assigned to one or more schedules.'

        Attributes:
            _id -- The id of the reminder.
            title -- The title of the reminder.
            description -- The description of the reminder.
            reminder_date -- The date of the reminder.
            _type -- The type of the reminder.
    """

    def __init__(self, element_id: str, title: str, description: str, reminder_date: datetime):
        """
        ReminderElement constructor.

        Arguments:
            element_id -- The id of the reminder.
            title -- The title of the reminder.
            description -- The description of the reminder.
            reminder_date -- The date of the reminder.
        """
        self._id = element_id
        self.title = title
        self.description = description
        self.reminder_date = reminder_date
        self._schedules = []
        self._type = "lembrete"

    def get_display_interval(self) -> (datetime, datetime):
        """
        Returns the interval that the reminder should ocupate in the calendar.
        In the case of the reminder, it will be 10 minutes before
        the reminder date untill the reminder date.
        Returns:
            (datetime, datetime) -- The interval that the reminder should ocupate in the calendar.
        """
        ending_date = self.reminder_date
        # The reminder will be displayed 10 minutes before the reminder date.
        starting_date = ending_date.replace(
            minute=ending_date.minute - 10)
        return (starting_date, ending_date)

    def get_type(self) -> str:
        """
        Returns the type of the reminder.

        Returns:
            str -- The type of the reminder.
        """
        return self._type

    def get_title(self) -> str:
        """
        Returns the title of the reminder.

        Returns:
            str -- The title of the reminder.
        """
        return self.title

    def get_schedules(self) -> list:
        """
        Returns the schedules of the reminder.

        Returns:
            list -- The schedules of the reminder.
        """
        return self._schedules

    def get_users(self) -> list:
        """
        Returns the users assigned to the reminder.

        Returns:
            list -- The users assigned to the reminder.
        """

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the reminder.

        Returns:
            dict -- The dictionary representation of the reminder.
        """
        return {
            "id": self._id,
            "title": self.title,
            "description": self.description,
            "reminder_date": self.reminder_date,
            "type": self._type,
            "schedules": self._schedules
        }
