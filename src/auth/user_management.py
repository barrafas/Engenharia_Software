import bcrypt

class UserManagement:
    """Handles user management (creation, editing, deletion)."""

    def __init__(self): ...

    def create_user(self, username, password):
        """
        Create a new user.

        Args:
            username (str): The username.
            password (str): The user's password.

        Returns:
            bool: True if the user was created successfully.
        """

        if not self.user_exists(username):
            hashed_password = self.hash_password(password)
            self.save_user_info(username, hashed_password)
            return True
        else:
            raise Exception('Usuário já existe')
    
    def delete_user(self, username):
        """
        Delete a user.

        Args:
            username (str): The username.

        Returns:
            bool: True if user deletion is successful.
        """
        # Lógica para excluir um usuário
        pass
        
    def user_exists(self, username): ...

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

    def save_user_info(self, username, hashed_password): ...