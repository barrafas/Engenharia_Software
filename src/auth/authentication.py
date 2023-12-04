"""
Authentication module

This module is responsible for authenticating users.

TODO:
    - PEP8 and PEP257 compliance
    - Refactor code
    - Add more tests
    - Add more documentation
    - Add more type hints
    - Add more error handling
    - Add more comments
    - Add logging
    - Fix docstrings

"""


import bcrypt
from ..user.user_management import UserManagement
from ..database.database_module import DatabaseModule

class Authentication:
    """
    User authentication module

    Attributes:
        database_module: Database module
        user_management_module: User management module

    Methods:
        authenticate_user: Authenticate user
        verify_password: Verify password
        logout_user: Logout user

    """

    def __init__(self, database_module: DatabaseModule):
        """
        Constructor for Authentication class

        Parameters:
            database_module: Database module
        """
        self.database_module = database_module
        self.user_management_module = UserManagement(self.database_module)

    def authenticate_user(self, username: str, password: str) -> bool:
        """
        Compare the input password with the hashed password in the database

        Parameters:
            username: Username - str
            password: Password - str
        """
        if not self.user_management_module.user_exists(username):
            print(f"Usuário {username} não encontrado!")
            return False
        else:
            user = self.user_management_module.get_user(username)
            user_password = user.get_hashed_password() if user else None

            if self.verify_password(password, user_password):
                print("✔ Autenticação bem-sucedida para o usuário:", username)
                return True
            else:
                print("❌ Falha na autenticação para o usuário:", username)
                return False

    def verify_password(self, input_password: str, hashed_password: str) -> bool:
        """
        Verify password

        Parameters:
            input_password: Input password
            hashed_password: Hashed password
        """
        return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def logout_user(self, username: str) -> None:
        """
        Logout user

        Parameters:
            username: Username
        """
        print("Usuário desconectado:", username)
