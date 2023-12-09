"""
    Interface for all calendar elements.

"""
from abc import ABC, abstractmethod
from datetime import datetime


class Element(ABC):
    """
        Interface for all calendar elements.

        Attributes:
            id: The id of the element.

        Methods:
            get_display_interval: Returns the interval that the event
            should ocupate in the calendar.
            get_type: Returns the type of the event.
            get_schedules: Returns the schedules of the event.
            to_dict: Returns a dictionary representation of the event.
    """
    @abstractmethod
    def get_display_interval(self) -> (datetime, datetime):
        """Returns the interval that the event should ocupate in the calendar.

        Arguments:
            datetime -- The start date of the event.
        """

    def get_schedules(self) -> list:
        """Returns the schedules of the event.

        Returns:
            list -- The schedules of the event.
        """

    @abstractmethod
    def get_users(self, filter_schedules = []) -> list:
        """Returns the users of the event.

        Arguments:
           filter_schedules -- The schedules to filter the users.

        Returns:
            list -- The users of the event.
        """

    @abstractmethod
    def set_title(self, title: str) -> None:
        """Sets the title of the event.

        Arguments:
            title {str} -- The title of the event.
        """

    @abstractmethod
    def set_description(self, description: str) -> None:
        """Sets the description of the event.

        Arguments:
            description {str} -- The description of the event.
        """

    @abstractmethod
    def to_dict(self) -> dict:
        """Returns a dictionary representation of the event.

        Returns:
            dict -- The dictionary representation of the event.
        """
