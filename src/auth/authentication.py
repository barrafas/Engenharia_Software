from ..database.database_module import DatabaseModule
from ..user.user_management import UserManagement
import bcrypt

# create a custom exception
class UserNotFound(Exception):
    pass

class AuthenticationModule:

    def __init__(self, database_module: DatabaseModule):
        self.database_module = database_module
        self.user_management_module = UserManagement(self.database_module)

    def authenticate_user(self, username: str, password: str) -> bool:
        if not self.user_management_module.user_exists(username):
            raise UserNotFound(f"Usuário {username} não encontrado!")
        else:
            user = self.user_management_module.get_user(username)
            user_password = user.get_hashed_password()

            if self.verify_password(password, user_password):
                return True
            else:
                return False

    def verify_password(self, input_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(input_password.encode(), hashed_password.encode())
