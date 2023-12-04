"""
UserManagement class
Responsible for managing the users in the database

Attributes:
    db: Database module
"""
import bcrypt
from ..database.database_module import DatabaseModule
from .user_model import User


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
    """

    def __init__(self, database_module: DatabaseModule):
        """
        Constructor for the UserManagement class

        Args:
            database_module: Database module
        """
        self.db = database_module

    def create_user(self, username: str, email: str, password: str,
                    user_id: str = None) -> User:
        """
        Create a new user

        Args:
            username: Username
            email: Email
            password: Password
            user_id: User ID

        Returns:
            The created user
        """

        if self.user_exists(username):
            raise UserAlreadyExistsError(f'Usuário {username} já existe')

        hashed_password = self.hash_password(password)
        hashed_password = hashed_password.decode('utf-8')

        if not user_id:
            user_id = self.db.get_next_id("users")

        user_info = {"user_id": user_id, "username": username,
                     "email": email, "password": hashed_password, "events": []}
        self.db.execute_query(
            {"entity": "users", "action": "insert", "data": user_info})

        user = User(user_id, username, email, hashed_password)
        return user

    def delete_user(self, username: str) -> None:
        """
        Delete a user

        Args:
            username: Username

        Returns:
            Void
        """

        if not self.user_exists(username):
            raise UserDoesNotExistError(f'Usuário {username} não existe')

        self.db.execute_query(
            {"entity": "users", "action": "delete", "criteria": {"username": username}})

    def user_exists(self, username: str) -> bool:
        """
        Check if a user exists

        Args:
            username: Username
        
        Returns:
            True if the user exists, False otherwise
        """
        query = {"entity": "users", "criteria": {"username": username}}
        data = self.db.fetch_data(query)
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

    def get_user(self, username: str) -> User or None:
        """
        Get a user

        Args:
            username: Username

        Returns:
            The user if it exists, None otherwise
        """
        query = {"entity": "users", "criteria": {"username": username}}
        data = self.db.fetch_data(query)
        return User.from_json(data[0]) if len(data) > 0 else None

    def update_user(self, user: str) -> None:
        """
        Update a user

        Args:
            user: User

        Returns:
            Void
        """

    def add_schedule_to_user(self, user_id: str, schedule_id: str) -> None:
        """Function to add a schedule to a user

        Arguments:
            user_id -- ID of the user
            schedule_id -- ID of the schedule

        Returns:
            None
        """
