import bcrypt
from src.database.database_module import DatabaseModule

class UserManagement:
    """Handles user management (creation, editing, deletion)."""

    def __init__(self, database_module: DatabaseModule):
        self.db = database_module

    def create_user(self, username, password):
        """
        Create a new user.

        Args:
            username (str): The username.
            password (str): The user's password.

        Returns:
            bool: True if the user was created successfully, False otherwise.
        """
        if not self.user_exists(username):
            print("\033[33m[INFO]\033[0m Usando módulo de documentos de texto")
            hashed_password = self.hash_password(password)
            hashed_password = hashed_password.decode('utf-8')
            user_info = {"username": username, "password": hashed_password}
            self.db.execute_query({"entity": "users", "action": "insert", "data": user_info})
            print("\033[33m[INFO]\033[0m Usuário criado com sucesso: ", user_info)
            return True
        else:
            raise Exception('Usuário já existe')
    
    def delete_user(self, username):
        """
        Delete a user.

        Args:
            username (str): The username.

        Returns:
            bool: True if user deletion is successful, False otherwise.
        """
        if self.user_exists(username):
            self.db.execute_query({"entity": "users", "action": "delete", "criteria": {"username": username}})
            return True
        else:
            raise Exception('Usuário não encontrado')
        
    def user_exists(self, username):
        """
        Check if a user exists.

        Args:
            username (str): The username.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        query = {"entity": "users", "criteria": {"username": username}}
        data = self.db.fetch_data(query)
        return len(data) > 0

    def hash_password(self, password):
        """
        Hashes the password.

        Args:
            password (str): The user's password.

        Returns:
            str: The hashed password.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password
    
    def save_user_info(self, username, hashed_password):
        """
        Save user information.

        Args:
            username (str): The username.
            hashed_password (str): The hashed password.
        """
        user_info = {"username": username, "password": hashed_password}
        hashed_password = hashed_password.decode('utf-8')
        self.db.execute_query({"entity": "users", "action": "insert", "data": user_info})

    def get_user(self, username):
        """
        Get a user.

        Args:
            username (str): The username.

        Returns:
            dict: The user information.
        """
        query = {"entity": "users", "criteria": {"username": username}}
        data = self.db.fetch_data(query)
        return data[0] if len(data) > 0 else None