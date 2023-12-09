from tests.test_users.mocks import Schedule, ScheduleManagement, \
                                   Element, ElementManagement
from datetime import datetime

class UserNotInSchedule(Exception):
    """
    Custom exception class for when a user already exists.
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

class User:
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
    def __init__(self, id: str, username: str, email: str, schedules: list=None, 
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
        self.id = id
        self.username = username
        self.email = email
        self.schedules = schedules if schedules else []
        self.hashed_password = hashed_password
        self.user_preferences = user_preferences if user_preferences else {}

    def __str__(self) -> str:
        return f"User({self.id}, {self.username}, {self.email}," \
        f"{self.schedules}, {self.user_preferences})"

    def to_dict(self) -> dict:
        """
        Create a dictionary with the user information

        Returns:
            A dictionary with the user information

        >>> user = User("id", "username", "email", ["id1", "id2"])
        >>> user.to_dict()
        {'id': 'id', 'username': 'username', 'email': 'email',
        'schedules': ['id1', 'id2'], 'password': None, 'user_preferences': {}}
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "schedules": self.schedules,
            "password": self.hashed_password,
            "user_preferences": self.user_preferences
        }
    
    def get_schedules(self) -> list:
        """
        Get the user schedules

        Returns:
            A list of schedules ids the user is a part of

        >>> user = User("id", "username", "email", ["id1", "id2"])
        >>> user.get_schedules()
        ['id1', 'id2']
        """
        return self.schedules
    
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
                        f"Usuário não está nessa agenda: {schedule}")
    
        schedule_management = ScheduleManagement.get_instance()
        elements = []
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
        return self.hashed_password
    
    def set_username(self, username: str):
        """
        Set the user name

        Args:
            username: user name            
        """
        if type(username) != str:
            raise TypeError("O nome de usuário deve ser uma string")
        elif username == "":
            raise UsernameCantBeBlank("O nome de usuário não pode ser vazio")
        else:
            self.username = username.strip()
    
    def set_email(self, email: str):
        """
        Set the user name

        Args:
            username: user name
        """
        if type(email) != str:
            raise TypeError("O email deve ser uma string")
        elif email == "":
            raise EmailCantBeBlank("O email não pode ser vazio")
        else:
            self.email = email.strip()

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
        if type(time) != tuple:
            raise TypeError("O horário deve ser uma tupla")
        if type(time[0]) != datetime or type(time[1]) != datetime:
            raise TypeError("A tupla de horário deve conter objetos datetime")

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