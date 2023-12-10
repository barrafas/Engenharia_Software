"""
Module to authenticate users

Classes:
    AuthenticationModule

Exceptions:
    UserNotFound
"""
import bcrypt

from ..database.database_module import DatabaseModule
from ..user.user_management import UserManagement

# create a custom exception
class UserNotFound(Exception):
    """Exception raised when user doesn't exist"""
    pass

class AuthenticationModule:
    """
    Class to authenticate users

    Methods:
        authenticate_user
        verify_password

    Attributes:
        database_module
        user_management_module
    """

    def __init__(self,
                database_module: DatabaseModule):
        """
        Constructor for AuthenticationModule

        Parameters:
            database_module (DatabaseModule): database module

        Attributes:
            database_module (DatabaseModule): database module
            user_management_module (UserManagement): user management module
        """
        self.database_module = database_module
        self.user_management_module = UserManagement(self.database_module)

    def authenticate_user(self,
                            username: str,
                            password: str) -> bool:
        """
        Function to authenticate user

        Parameters: 
            username (str): username
            password (str): password

        Returns:
            bool: True if user is authenticated, False otherwise
        """
        if not self.user_management_module.user_exists(username):
            raise UserNotFound(f"Usuário {username} não encontrado!")
        else:
            user = self.user_management_module.get_user(username)
            user_password = user.get_hashed_password()

            if self.verify_password(password, user_password):
                return True
            else:
                return False

    def verify_password(self,
                        input_password: str,
                        hashed_password: str) -> bool:
        """
        Function to verify password

        Parameters:
            input_password (str): input password
            hashed_password (str): hashed password

        Returns:
            bool: True if password is correct, False otherwise
        """
        return bcrypt.checkpw(input_password.encode(),
                              hashed_password.encode())
