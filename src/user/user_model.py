from tests.test_users.mocks import Schedule, ScheduleManagement, \
                                   Element, ElementManagement
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
        schedules and elements

        Args:
            time: tuple with the start and end time to be checked

        Returns:
            True if the user is available, False otherwise
        """
        element_ids = self.get_elements()



        # fazer query no banco de dados comparando o horário com os horários
        # dos elementos da seguinte forma:
        # verificar se em algum dos elementos, a condição
        #  time[0] > element.end_time ou time[1] < element.start_time é falsa.
        return


    def __repr__(self):
        return " <User>:"+str(self.to_dict())