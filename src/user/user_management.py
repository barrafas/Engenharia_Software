"""
UserManagement class
Responsible for managing the users in the database

Attributes:
    db: Database module
    users: Dict of users, where the key is the id
"""
import bcrypt
from src.database.mongo_module import MongoModule, DuplicatedIDError
from src.database.mongo_module import NonExistentIDError
from src.observer.observer import Observer, Subject, DatabaseNotProvidedError
from .user_model import User, UsernameCantBeBlank

class UserAlreadyExistsError(Exception):
    """
    Custom exception class for when a user already exists.
    """

class UserManagement(Observer):
    """
    UserManagement class
    Responsible for managing the users in the database

    Attributes:
        db: Database module
        users: Dict of users, where the key is the id
    """
    _instance = None

    @classmethod
    def get_instance(cls,
                    database_module: MongoModule = None,
                    users: dict = None) -> 'UserManagement':
        """
        Get the instance of the UserManagement class
        """
        if not cls._instance:
            cls._instance = cls(database_module, users)
        return cls._instance

    def __init__(self,
                database_module: MongoModule,
                users: dict = None):
        """
        Constructor for the UserManagement class

        Args:
            database_module: Database module
        """

        if not database_module:
            raise DatabaseNotProvidedError(
                "Database module not provided on object creation.")
        
        self.db_module = database_module
        self.users = users if users is not None else {}

    def create_user(self, username: str, email: str, password: str,
                    user_preferences: dict = None, user_id: str = None) -> User:
        """
        Create a new user

        Args:
            username: Username
            email: Email
            password: Password
            user_preferences: User preferences
            id: User ID

        Returns:
            The created user
        """
        username = username.strip()
        email = email.strip()

        if username == "":
            raise UsernameCantBeBlank("Username cannot be blank")

        if self.user_exists(user_id):
            raise DuplicatedIDError(f'User {user_id} already exists')

        hashed_password = self.hash_password(password)
        hashed_password = hashed_password.decode('utf-8')

        user_info = {"_id": user_id,
                    "username": username,
                     "email": email, "schedules": [], 
                     "hashed_password": hashed_password, 
                     "user_preferences": user_preferences}

        self.db_module.insert_data('users', {**user_info})

        user = User(**user_info)
        self.users[user_id] = user
        user.attach(self)
        return user

    def delete_user(self, user_id: str) -> None:
        """
        Delete a user

        Args:
            user_id: User ID

        Returns:
            Void
        """

        if not self.user_exists(user_id):
            raise NonExistentIDError(f'User {user_id} does not exist')

        user = self.get_user(user_id)
        # Update each schedule
        from src.schedule.schedule_management import ScheduleManagement
        schedule_manager = ScheduleManagement.get_instance()
        for schedule in user.schedules:
            schedule_instance = schedule_manager.get_schedule(schedule)
            new_permissions = schedule_instance.permissions
            new_permissions.pop(user_id)
            schedule_instance.permissions = new_permissions

        self.db_module.delete_data('users', {"_id": user_id})
        if user_id in self.users:
            remove = self.users.pop(user_id)
            del remove

    def user_exists(self, user_id: str) -> bool:
        """
        Check if a user exists

        Args:
            user_id: User ID
        
        Returns:
            True if the user exists, False otherwise
        """
        data = self.db_module.select_data('users', {"_id": user_id})
        return len(data) > 0

    def hash_password(self, password: str) -> str:
        """
        Hash a password

        Args:
            password: Password

        Returns:
            The hashed password
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def get_user(self, user_id: str) -> User:
        """
        Get a user

        Args:
            user_id: User ID

        Returns:
            The user if it exists, None otherwise
        """
        data = self.db_module.select_data('users', {"_id": user_id})
        print(data[0])
        user = User(**data[0])
        user.attach(self)
        print(user)
        self.users[user_id] = user
        return user

    def update_user(self, user_id: str) -> None:
        """
        Updates a user in the db based on its current local state

        Args:
            user_id: User ID

        Returns:
            Void
        """
        if not self.user_exists(user_id):
            raise NonExistentIDError(f'User {user_id} does not exist')

        user = self.users[user_id]
        user_info = user.to_dict()
        self.db_module.update_data('users', {"_id": user_id}, user_info)
        return



    def add_schedule_to_user(self, user_id: str, schedule_id: str,
                             permission:str) -> None:
        """Function to add a schedule to a user

        Arguments:
            user_id -- ID of the user
            schedule_id -- ID of the schedule
            permission -- Permission of the user in the schedule

        Returns:
            None
        """
        from src.schedule.schedule_management import ScheduleManagement
        schedule_manager = ScheduleManagement.get_instance()
        if not self.user_exists(user_id):
            raise NonExistentIDError(f'User {user_id} does not exist')


        user = self.get_user(user_id)
        if schedule_id not in user.schedules:
            user.schedules = user.schedules + [schedule_id]
            schedule = schedule_manager.get_schedule(schedule_id)
            schedule.permissions = {**schedule.permissions, user_id: permission}
        else:
            raise DuplicatedIDError(f'Usuário {user_id} já está no schedule \
                                    {schedule_id}')
        return

    def update(self, user: Subject) -> None:
        """
        Called when the user is updated.

        Args:
            user: The user that was updated.
        """
        print(f"User {user.id} was updated.")
        self.update_user(user.id)
