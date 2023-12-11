"""
module that contains the User class and its exceptions.
The User class represents a user of the application.

Classes:

    UserNotInSchedule -- Exception raised when a user is not in a schedule.

    UsernameCantBeBlank -- Exception raised when a username is blank.

    EmailCantBeBlank -- Exception raised when a email is blank.

    User -- Class that represents a user of the application.
"""


from datetime import datetime
from src.schedule.schedule_management import ScheduleManagement
from src.calendar_elements.element_management import ElementManagement
from src.observer.observer import Observer, Subject


class UserNotInSchedule(Exception):
    """
    Custom exception class for when a user is not in a schedule.
    """
class UsernameCantBeBlank(Exception):
    """
    Custom exception class for when a username is blank.
    """
class EmailCantBeBlank(Exception):
    """
    Custom exception class for when a email is blank.
    """

class TupleWithLessThanTwoDatetimeObjects(Exception):
    """
    Custom exception class for when a tuple with less than two datetime objects
    is passed to the check_disponibility method.
    """

class User(Subject):
    """
    User class

    Attributes:
        id: user id
        username: user name
        email: user email
        schedules: list of schedules ids
        hashed_password: user hashed password
        user_preferences: user preferences
    """
    def __init__(self, _id: str, username: str, email: str, schedules: list=None,
                 hashed_password: str=None, user_preferences: dict=None):
        """
        Constructor for the User class

        Args:
            id: user id
            username: user name
            email: user email
            schedules: list of schedules ids
            hashed_password: user hashed password
            user_preferences: user preferences
        """
        self.__observers = []
        self.__id = _id
        self.username = username
        self.email = email
        self.__schedules = schedules if schedules else []
        self.__hashed_password = hashed_password
        self.user_preferences = user_preferences if user_preferences else {}

    def __str__(self) -> str:
        return f"User({self.__id}, {self.username}, {self.email}," \
        f"{self.schedules}, {self.user_preferences})"

    @property
    def id(self) -> str:
        """ method that returns the id of the user"""
        return self.__id

    @property
    def schedules(self) -> list:
        """ method that returns the schedules of the user"""
        return self.__schedules

    @property
    def observers(self):
        """ method that returns the observers of the user """
        return self.__observers

    @schedules.setter
    def schedules(self, schedules: [str]):
        """Sets the schedules of the event."""
        self.__schedules = schedules
        self.notify()

    def to_dict(self) -> dict:
        """
        Create a dictionary with the user information

        Returns:
            A dictionary with the user information

        >>> user = User("id", "username", "email", ["id1", "id2"])
        >>> user.to_dict()
        {'_id': 'id', 'username': 'username', 'email': 'email',
        'schedules': ['id1', 'id2'], 'password': None, 'user_preferences': {}}
        """
        return {
            "_id": self.__id,
            "username": self.username,
            "email": self.email,
            "schedules": self.schedules,
            "password": self.__hashed_password,
            "user_preferences": self.user_preferences
        }

    def get_schedules(self) -> list:
        """
        Get the user schedules

        Returns:
            A list of schedules instances the user has access to
        """
        schedule_management = ScheduleManagement.get_instance()
        schedules = []
        for schedule_id in self.schedules:
            schedules.append(schedule_management.get_schedule(schedule_id))
        return schedules

    def get_elements(self, schedules: list=None) -> list:
        '''
        Get all elements from the user schedules, without repetition, or
        from a list of filtered schedules

        Args:
            schedules: list of schedules ids

        Returns:
            A list of elements ids the user is a part of
        '''
        if not schedules:
            schedules = self.get_schedules()
        else:
            for schedule in schedules:
                if schedule not in self.get_schedules():
                    raise UserNotInSchedule(
                        f"User isn't in: {schedule}")

        schedule_management = ScheduleManagement.get_instance()
        elements = []
        if not schedules:
            schedules = self.schedules
        for schedule in schedules:
            schedule = schedule_management.get_schedule(schedule)
            elements += schedule.get_elements()

        elements = list(set(elements))
        return elements

    def get_hashed_password(self) -> str:
        """
        Get the user hashed password

        Returns:
            The user hashed password

        >>> user = User("id", "username", "email", ["id1", "id2"], "hashed_password")
        >>> user.get_hashed_password()
        'hashed_password'
        """
        return self.__hashed_password

    def set_username(self, username: str):
        """
        Set the user name

        Args:
            username: user name 

        >>> user = User("id", "username", "email", ["id1", "id2"])
        >>> user.set_username("new_username")
        >>> user.username
        'new_username'           
        """
        if isinstance(username, str) is False:
            raise TypeError("Username must be a string")
        elif username == "":
            raise UsernameCantBeBlank("Username cannot be blank")
        else:
            self.username = username.strip()
            self.notify()

    def set_email(self, email: str):
        """
        Set the user name

        Args:
            username: user name

        >>> user = User("id", "username", "email", ["id1", "id2"])
        >>> user.set_email("new_email")
        >>> user.email
        'new_email'
        """
        if isinstance(email, str) is False:
            raise TypeError("Email must be a string")
        elif email == "":
            raise EmailCantBeBlank("Email cannot be blank")
        else:
            self.email = email.strip()
            self.notify()

    def set_preferences(self, preferences: dict):
        """
        Set the user preferences

        Args:
            preference_type: preference type
            preference: preference to be set
        """
        for preference_type, preference in preferences.items():
            if isinstance(preference_type, str) is False:
                raise TypeError("The preference must be a string")
            else:
                self.user_preferences[preference_type] = preference
                self.notify()


    def check_disponibility(self, time: tuple) -> bool:
        """
        Checks if the user is available at a given time, based on the user's
        schedules and elements. It should not raise a conflict if the type
        of the element is not 'evento'.

        Args:
            time: tuple with the start and end time to be checked

        Returns:
            True if the user is available, False otherwise
        """
        if isinstance(time, tuple) is False:
            raise TypeError("Time must be a tuple")
        if len(time) < 2:
            raise TupleWithLessThanTwoDatetimeObjects(
                "The tuple must have at least two datetime objects")
        if (isinstance(time[0], datetime) is False) or \
                (isinstance(time[1], datetime) is False):
            raise TypeError("The tuple must have datetime objects")

        element_ids = self.get_elements()
        element_management = ElementManagement.get_instance()

        for element_id in element_ids:
            element = element_management.get_element(element_id)
            if element.type != 'evento':
                continue

            # Check if the start time of the element is within the given time period
            if time[0] <= element.start_time < time[1]:
                return False

            # Check if the end time of the element is within the given time period
            if time[0] < element.end_time <= time[1]:
                return False

            # Check if the given time period is within the start
            # and end time of the element
            if element.start_time <= time[0] < element.end_time or \
                element.start_time < time[1] <= element.end_time:
                return False

        return True

    def __repr__(self):
        return " <User>:"+str(self.to_dict())

    def attach(self, observer: Observer) -> None:
        """
            Attach an observer to the subject.

            Arguments:
                observer -- the observer to attach.
        """
        self.__observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """
            Detach an observer from the subject.

            Arguments:
                observer -- the observer to detach.
        """
        self.__observers.remove(observer)

    def notify(self) -> None:
        """
            Notify all the observers that the subject has changed.
        """
        for observer in self.__observers:
            observer.update(self)
