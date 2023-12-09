"""
UserManagement class
Responsible for managing the users in the database

Attributes:
    db: Database module
    users: Dict of users, where the key is the id
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
        users: Dict of users, where the key is the id
    """

    def __init__(self, database_module: DatabaseModule):
        """
        Constructor for the UserManagement class

        Args:
            database_module: Database module
        """
        self.db = database_module
        self.users = {}

    def create_user(self, username: str, email: str, password: str,
                    user_preferences: dict, id: str = None) -> User:
        """
        Create a new user

        Args:
            username: Username
            email: Email
            password: Password
            id: User ID

        Returns:
            The created user
        """

        if self.user_exists(username):
            raise UserAlreadyExistsError(f'Usuário {username} já existe')


        hashed_password = self.hash_password(password)
        hashed_password = hashed_password.decode('utf-8')

        if not id:
            id = self.db.get_next_id("users")

        user_info = {"id": id, "username": username,
                     "email": email, "schedules": [], 
                     "hashed_password": hashed_password, "user_preferences": user_preferences}
        self.db.execute_query(
            {"entity": "users", "action": "insert", "data": user_info})

        user = User(**user_info)
        self.users[id] = user
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

    def get_user(self, username: str) -> User:
        """
        Get a user

        Args:
            username: Username

        Returns:
            The user if it exists, None otherwise
        """
        query = {"entity": "users", "criteria": {"username": username}}
        data = self.db.fetch_data(query)
        user = User(**data[0])
        self.users[user.id] = user
        return 

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
        self.db.execute_query(
            {"entity": "users", "action": "update", "data": user_info})
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
