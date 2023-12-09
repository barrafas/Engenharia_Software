"""
    This module contains the classes that represent the different types of
    elements that can be displayed in the calendar.
"""
from datetime import datetime, timedelta
from .element_interface import CalendarElement
from src.user.user_model import User

class Schedule:
    """Mock class for Schedule"""
    def __init__(self, id, title, description, permissions, elements):
        self.__id = id
        self.tilte = "title"
        self.description = "description"
        self.__permissions = permissions
        self.__elements = elements

    @property
    def id(self):
        return self.__id

    @property
    def permissions(self):
        return self.__permissions

    @property
    def elements(self):
        return self.__elements


class ScheduleManagement:
    """Mock class for ScheduleManagement"""

    __instance = None

    def __init__(self):
        self.__schedules = {}

    def get_schedule(self, id: str) -> Schedule:
        ... 
    
    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = ScheduleManagement()
        return cls.__instance

class UserManagement:
    """Mock class for UserManagement"""

    __instance = None

    def __init__(self):
        self.__users = {}

    def get_user(self, id: str) -> Schedule:
        ... 
    
    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = UserManagement()
        return cls.__instance
  



class EventElement(CalendarElement):
    """
    A class that represents an event.

    'Event with determined beginning and end dates, which can be
    scheduled for a specific time, and which can be
    assigned to one or more schedules.'
    """

    def __init__(self, 
                element_id: str,
                title: str,
                start: datetime,
                end: datetime,
                schedules: [str],
                description: str = None,
                element_type: str = "event"):
        """
        EventElement constructor.

        Arguments:
            element_id -- The id of the event.
            title -- The title of the event.
            description -- The description of the event.
            start -- The start date of the event.
            end -- The end date of the event.
            schedules -- The schedules that the event is assigned to.
            type -- The type of the event.
        """
        self.__schedules = schedules if schedules else []
        self.__element_type = element_type

        self.__id = element_id
        self.set_title(title)
        self.set_description(description)
        self.set_interval(start, end)

    @property
    def id(self):
        """Returns the id of the event. """
        return self.__id

    @property
    def schedules(self):
        """Returns the schedules of the event."""
        return self.__schedules

    @property
    def type(self):
        """Returns the type of the event."""
        return self.__element_type

    def get_display_interval(self) -> (datetime, datetime):
        """
        Returns the interval that the event should ocupate in the calendar.

        Returns:
            (datetime, datetime) -- The interval that the event should ocupate 
            in the calendar.
        """
        return (self.start, self.end)

    def get_schedules(self) -> list:
        """
        Returns the schedules of the event.

        Returns:
            [schedule] -- The schedules of the event.
        """
        schedule_manager = ScheduleManagement.get_instance()
        return [schedule_manager.get_schedule(id) for id in self.__schedules]  # Return a list of Schedules objects

    def get_users(self, filter_schedules = []) -> list:
        """
        Returns the users that are assigned to the event.

        Arguments:
            filter_schedules -- A list of schedules to filter the users.

        Returns:
            [user] -- The users that are assigned to the reminder.
        """
        schedule_manager = ScheduleManagement.get_instance()
        filter_schedules = [schedule for schedule in self.__schedules
                                if schedule in filter_schedules]
        users = []
        for schedule_id in filter_schedules:
            schedule = schedule_manager.get_schedule(schedule_id)
            users += list(schedule.permissions.keys())
        
        user_manager = UserManagement.get_instance()

        users = [user_manager.get_user(id) for id in users]
        return users

    def set_interval(self, start: datetime, end: datetime) -> None:
        """
        Sets the interval of the event.

        Arguments:
            start -- start date of the event.
            end -- end date of the event.
        """
        if start is None:
            raise ValueError("Start cannot be None")
        elif not isinstance(start, datetime):
            raise TypeError("Start must be a datetime object")
        elif end is None:
            raise ValueError("End cannot be None")
        elif not isinstance(end, datetime):
            raise TypeError("End must be a datetime object")
        elif start >= end:
            raise ValueError("Start must be before end")
        else:
            self.start = start
            self.end = end

    def set_title(self, title: str) -> None:
        """
        Sets the title of the event.

        Arguments:
            title -- title of the event.
        """

        if title is None:
            raise ValueError("Title cannot be None")
        elif not isinstance(title, str):
            raise TypeError("Title must be a string")
        elif not title.strip():
            raise ValueError("Title cannot be empty or blank")
        elif len(title) > 50:
            raise ValueError("Title cannot have more than 50 characters")
        else:   
            self.title = title

    def set_description(self, description: str) -> None:
        """
        Sets the description of the event.

        Arguments:
            description -- description of the event.
        """
        if description is not None:
            if not isinstance(description, str):
                raise TypeError("Description must be a string")
            elif len(description) > 500:
                raise ValueError("Description cannot have more than 500 characters")
        self.description = description

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the event.

        Returns:
            dict -- The dictionary representation of the event.
        """
        return {
            "id": self.__id,
            "title": self.title,
            "start": self.start,
            "end": self.end,
            "element_type": self.__element_type,
            "description": self.description,
            "schedules": self.__schedules
        }


class TaskElement(CalendarElement):
    """
    A class that represents a task.

    'Task with a deadline, which can be scheduled for a specific
    time, and which can be assigned to one or more schedules.'
    """

    def __init__(self,
                element_id: str,
                title: str,
                due_date: datetime,
                schedules: [str],
                description: str = None,
                state: str = None,
                element_type: str = "task"):
        """
        TaskElement constructor.

        Arguments:
            element_id -- The id of the task.
            title -- The title of the task.
            due_date -- The due date of the task.
            schedules -- The schedules that the task is assigned to.
            description -- The description of the task.
            state -- The state of the task.
            element_type -- The type of the task.
        """
        self.__schedules = schedules if schedules else []
        self.__element_type = element_type

        self.__id = element_id
        self.set_state(state)
        self.set_title(title)
        self.set_description(description)
        self.set_due_date(due_date)

    @property
    def id(self):
        """Returns the id of the task."""
        return self.__id

    @property
    def schedules(self):
        """Returns the schedules of the task."""
        return self.__schedules

    @property
    def type(self):
        """Returns the type of the task."""
        return self.__element_type

    def get_display_interval(self) -> (datetime, datetime):
        """
        Returns the interval that the task should ocupate in the calendar.
        In the case of the task, it will be 10 minutes before
        the due date untill the due date.

        Returns:
            (datetime, datetime) -- The interval that the task should ocupate 
            in the calendar.
        """
        ending_date = self.due_date
        # The task will be displayed 10 minutes before the due date.
        ten_minutes = timedelta(minutes=10)
        starting_date = ending_date - ten_minutes

        return (starting_date, ending_date)

    def get_schedules(self) -> list:
        """
        Returns the schedules of the task.

        Returns:
            [schedules] -- The schedules of the task.
        """
        schedule_manager = ScheduleManagement.get_instance()
        return [schedule_manager.get_schedule(id) for id in self.__schedules]

    def get_users(self, filter_schedules = []) -> list:
        """
        Returns the users that are assigned to the task.

        Arguments:
            filter_schedules -- A list of schedules to filter the users.

        Returns:
            [user] -- The users that are assigned to the task.
        """
        schedule_manager = ScheduleManagement.get_instance()
        schedules_to_use = filter_schedules or self.__schedules
        
        users = set()
        for schedule_id in schedules_to_use:
            schedule = schedule_manager.get_schedule(schedule_id)
            users.update(schedule.permissions.keys())
        
        user_manager = UserManagement.get_instance()
        return [user_manager.get_user(id) for id in users]

    def set_due_date(self, due_date: datetime) -> None:
        """
        Sets the due date of the task.

        Arguments:
            due_date -- due date of the task.
        """
        if due_date is None:
            raise ValueError("Due date cannot be None")
        elif not isinstance(due_date, datetime):
            raise TypeError("Due date must be a datetime object")
        else:
            self.due_date = due_date

    def set_state(self, state: str):
        """
        Sets the state of the task.

        Arguments:
            state -- The new state of the task.
        """
        if state is None:
            self.state = 'incomplete'
        else:
            if not isinstance(state, str):
                raise TypeError("State must be a string")
            elif state not in ["incomplete", "complete", "cancelled"]:
                raise ValueError("State must be either 'incomplete' or 'complete' or 'cancelled'")
            else:
                self.state = state

    def set_title(self, title: str) -> None:
        """
        Sets the title of the task.

        Arguments:
            title -- title of the task.
        """

        if title is None:
            raise ValueError("Title cannot be None")
        elif not isinstance(title, str):
            raise TypeError("Title must be a string")
        elif not title.strip():
            raise ValueError("Title cannot be empty or blank")
        elif len(title) > 50:
            raise ValueError("Title cannot have more than 50 characters")
        else:
            self.title = title

    def set_description(self, description: str) -> None:
        """
        Sets the description of the task.

        Arguments:
            description -- description of the task.
        """
        if description is not None:
            if not isinstance(description, str):
                raise TypeError("Description must be a string")
            elif len(description) > 500:
                raise ValueError("Description cannot have more than 500 characters")
        self.description = description

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the task.

        Returns:
            dict -- The dictionary representation of the task.
        """
        return {
            "id": self.__id,
            "title": self.title,
            "description": self.description,
            "state": self.state,
            "due_date": self.due_date,
            "element_type": self.__element_type,
            "schedules": self.__schedules
        }
    
class ReminderElement(CalendarElement):
    """
    A class that represents a reminder.

    'Reminder with a date and time, which can be scheduled for a specific
    time, and which can be assigned to one or more schedules.'
    """

    def __init__(self,
                element_id: str,
                title: str,
                reminder_date: datetime,
                schedules: [str],
                description: str = None,
                element_type: str = "reminder"):
        """
        ReminderElement constructor.

        Arguments:
            element_id -- The id of the reminder.
            title -- The title of the reminder.
            reminder_date -- The date of the reminder.
            schedules -- The schedules that the reminder is assigned to.
            description -- The description of the reminder.
            element_type -- The type of the reminder.
        """
        self.__schedules = schedules if schedules else []
        self.__element_type = element_type

        self.__id = element_id
        self.set_title(title)
        self.set_description(description)
        self.set_reminder_date(reminder_date)

    @property
    def id(self):
        """Returns the id of the reminder."""
        return self.__id

    @property
    def schedules(self):
        """Returns the schedules of the reminder."""
        return self.__schedules

    @property
    def type(self):
        """Returns the type of the reminder."""
        return self.__element_type

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
        ten_minutes = timedelta(minutes=10)
        starting_date = ending_date - ten_minutes

        return (starting_date, ending_date)

    def get_schedules(self) -> list:
        """
        Returns the schedules of the reminder.

        Returns:
            list -- The schedules of the reminder.
        """
        schedule_manager = ScheduleManagement.get_instance()
        # Return a list of Schedules objects
        return [schedule_manager.get_schedule(id) for id in self.__schedules]

    def get_users(self, filter_schedules) -> list:
        """
        Returns the users that are assigned to the reminder.

        Returns:
            [user] -- The users that are assigned to the reminder.
        """
    
    def set_reminder_date(self, reminder_date: datetime) -> None:
        """
        Sets the reminder date of the reminder.

        Arguments:
            reminder_date -- reminder date of the reminder.
        """
        if reminder_date is None:
            raise ValueError("Reminder date cannot be None")
        elif not isinstance(reminder_date, datetime):
            raise TypeError("Reminder date must be a datetime object")
        else:
            self.reminder_date = reminder_date

    def set_title(self, title: str) -> None:
        """
        Sets the title of the reminder.

        Arguments:
            title -- title of the reminder.
        """

        if title is None:
            raise ValueError("Title cannot be None")
        elif not isinstance(title, str):
            raise TypeError("Title must be a string")
        elif not title.strip():
            raise ValueError("Title cannot be empty or blank")
        elif len(title) > 50:
            raise ValueError("Title cannot have more than 50 characters")
        else:   
            self.title = title

    def set_description(self, description: str) -> None:
        """
        Sets the description of the reminder.

        Arguments:
            description -- description of the reminder.
        """
        if description is not None:
            if not isinstance(description, str):
                raise TypeError("Description must be a string")
            elif len(description) > 500:
                raise ValueError("Description cannot have more than 500 characters")
        self.description = description

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the reminder.

        Returns:
            dict -- The dictionary representation of the reminder.
        """
        return {
            "id": self.__id,
            "title": self.title,
            "description": self.description,
            "reminder_date": self.reminder_date,
            "element_type": self.__element_type,
            "schedules": self.__schedules
        }
