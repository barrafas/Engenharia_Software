"""
    This module contains the classes that represent the different types of
    elements that can be displayed in the calendar.
"""
from datetime import datetime, timedelta
from .element_interface import CalendarElement


class EventElement(CalendarElement):
    """
        A class that represents an event.

        'Event with determined beginning and end dates, which can be
        scheduled for a specific time, and which can be
        assigned to one or more schedules.'
    """

    def __init__(self, element_id: str, title: str, start: datetime, end: datetime, 
                 description: str = None, schedules: [str] = None, type: str = "event"):
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
        self.__type = type

        self.__id = element_id
        self.set_title(title)
        self.set_description(description)
        self.set_interval(start, end)

    @property
    def id(self):
        return self.__id
    
    @property
    def schedules(self):
        return self.__schedules
    
    @property
    def type(self):
        return self.__type

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
        return self.__type

    def get_schedules(self) -> list:
        """
        Returns the schedules of the event.

        Returns:
            list -- The schedules of the event.
        """
        pass
    
    def get_users(self, schedules = []) -> [str]:
        """
        Returns the users that are assigned to the event.

        Returns:
            [str] -- The users that are assigned to the event.
        """
        pass
    
    def set_interval(self, start: datetime, end: datetime) -> None:
        '''
            Sets the interval of the event.

            Arguments:
                start -- start date of the event.
                end -- end date of the event.
        '''
        if start is None:
            raise ValueError("Start cannot be None")
        elif type(start) != datetime:
            raise TypeError("Start must be a datetime object")
        elif end is None:
            raise ValueError("End cannot be None")
        elif type(end) != datetime:
            raise TypeError("End must be a datetime object")
        elif start >= end:
            raise ValueError("Start must be before end")
        else:
            self.start = start
            self.end = end

    def set_title(self, title: str) -> None:
        '''
            Sets the title of the event.

            Arguments:
                title -- title of the event.
        '''

        if title is None:
            raise ValueError("Title cannot be None")
        elif type(title) != str:
            raise TypeError("Title must be a string")
        elif not title.strip():
            raise ValueError("Title cannot be empty or blank")
        elif len(title) > 50:
            raise ValueError("Title cannot have more than 50 characters")
        else:   
            self.title = title

    def set_description(self, description: str) -> None:
        '''
            Sets the description of the event.

            Arguments:
                description -- description of the event.
        '''
        if description is not None:
            if type(description) != str:
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
            "type": self.__type,
            "description": self.description,
            "schedules": self.__schedules
        }


class TaskElement(CalendarElement):
    """
        A class that represents a task.

        'Task with a deadline, which can be scheduled for a specific
        time, and which can be assigned to one or more schedules.'
    """

    def __init__(self, element_id: str, title: str, due_date: datetime, 
                description: str = None, state: str = None,
                schedules: [str] = None, type: str = "task"):
        """
        TaskElement constructor.

        Arguments:
            element_id -- The id of the task.
            title -- The title of the task.
            description -- The description of the task.
            due_date -- The due date of the task.
        """
        self.__schedules = schedules if schedules else []
        self.__type = type

        self.__id = element_id
        self.set_state(state)
        self.set_title(title)
        self.set_description(description)
        self.set_due_date(due_date)

    @property
    def id(self):
        return self.__id
    
    @property
    def schedules(self):
        return self.__schedules
    
    @property
    def type(self):
        return self.__type

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
        ten_minutes = timedelta(minutes=10)
        starting_date = ending_date - ten_minutes

        return (starting_date, ending_date)

    def get_type(self) -> str:
        """
        Returns the type of the task.

        Returns:
            str -- The type of the task.
        """
        return self.__type

    def get_schedules(self) -> list:
        """
        Returns the schedules of the task.

        Returns:
            list -- The schedules of the task.
        """
        pass

    def get_users(self, schedules = []) -> [str]:
        """
        Returns the users that are assigned to the task.

        Returns:
            [str] -- The users that are assigned to the task.
        """
        pass
    
    def set_due_date(self, due_date: datetime) -> None:
        '''
            Sets the due date of the task.

            Arguments:
                due_date -- due date of the task.
        '''
        if due_date is None:
            raise ValueError("Due date cannot be None")
        elif type(due_date) != datetime:
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
            if type(state) != str:
                raise TypeError("State must be a string")
            elif state not in ["incomplete", "complete", "cancelled"]:
                raise ValueError("State must be either 'incomplete' or 'complete' or 'cancelled'")
            else:
                self.state = state

    def set_title(self, title: str) -> None:
        '''
            Sets the title of the task.

            Arguments:
                title -- title of the task.
        '''

        if title is None:
            raise ValueError("Title cannot be None")
        elif type(title) != str:
            raise TypeError("Title must be a string")
        elif not title.strip():
            raise ValueError("Title cannot be empty or blank")
        elif len(title) > 50:
            raise ValueError("Title cannot have more than 50 characters")
        else:   
            self.title = title

    def set_description(self, description: str) -> None:
        '''
            Sets the description of the task.

            Arguments:
                description -- description of the task.
        '''
        if description is not None:
            if type(description) != str:
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
            "type": self.__type,
            "schedules": self.__schedules
        }
