"""
UserManagement class
Responsible for managing the users in the database

Attributes:
    db: Database module
    users: Dict of users, where the key is the id
"""
import bcrypt
from src.database.mongo_module import MongoModule
from .user_model import User, UsernameCantBeBlank

class UserAlreadyExistsError(Exception):
    """
    Custom exception class for when a user already exists.
    """


class UserDoesNotExistError(Exception):
    """
    Custom exception class for when a user does not exist.
    """


class UserManagement:
    """
    UserManagement class
    Responsible for managing the users in the database

    Attributes:
        db: Database module
        users: Dict of users, where the key is the id
    """
    _instance = None

    @classmethod
    def get_instance(cls, database_module: MongoModule):
        if not cls._instance:
            cls._instance = cls(database_module)
        return cls._instance

    def __init__(self, database_module: MongoModule):
        """
        Constructor for the UserManagement class

        Args:
            database_module: Database module
        """
        self.db = database_module
        self.users = {}

    def create_user(self, username: str, email: str, password: str,
                    user_preferences: dict = None, id: str = None) -> User:
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
            raise UsernameCantBeBlank("Nome de usuário não pode ser vazio")

        if self.user_exists(username):
            raise UserAlreadyExistsError(f'Usuário {username} já existe')

        hashed_password = self.hash_password(password)
        hashed_password = hashed_password.decode('utf-8')

        # if not id:
        #     id = self.db.get_next_id("users")

        user_info = {"_id": id,
                    "username": username,
                     "email": email, "schedules": [], 
                     "hashed_password": hashed_password, 
                     "user_preferences": user_preferences}
        
        self.db.insert_data('users', {**user_info})

        user = User(**user_info)
        self.users[id] = user
        return user

    def delete_user(self, id: str) -> None:
        """
        Delete a user

        Args:
            username: Username

        Returns:
            Void
        """

        if not self.user_exists(id):
            raise UserDoesNotExistError(f'Usuário {id} não existe')

        self.db.delete_data('users', {"_id": id})

    def user_exists(self, id: str) -> bool:
        """
        Check if a user exists

        Args:
            username: Username
        
        Returns:
            True if the user exists, False otherwise
        """
        data = self.db.select_data('users', {"_id": id})
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

    def get_user(self, id: str) -> User:
        """
        Get a user

        Args:
            username: Username

        Returns:
            The user if it exists, None otherwise
        """
        data = self.db.select_data('users', {"_id": id})
        print(data[0])
        user = User(**data[0])
        print(user)
        self.users[user._id] = user
        return user

    def update_user(self, id: str) -> None:
        """
        Updates a user in the db based on its current local state

        Args:
            user: User

        Returns:
            Void
        """
        if not self.user_exists(id):
            raise UserDoesNotExistError(f'Usuário {id} não existe')
        
        user = self.users[id]
        user_info = user.to_dict()
        self.db.update_data('users', {"_id": id}, user_info)
        return



    def add_schedule_to_user(self, user_id: str, schedule_id: str) -> None:
        """Function to add a schedule to a user

        Arguments:
            user_id -- ID of the user
            schedule_id -- ID of the schedule

        Returns:
            None
        """
        if not self.user_exists(user_id):
            raise UserDoesNotExistError(f'Usuário {user_id} não existe')

        user = self.users[user_id]
        user.schedules.append(schedule_id)
        self.update_user(user_id)
        return
