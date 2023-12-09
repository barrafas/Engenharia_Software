from ..database.database_module import DatabaseModule

class Authentication:

    def __init__(self, database_module: DatabaseModule):
        ...

    def authenticate_user(self, username: str, password: str) -> bool:
        ...

    def verify_password(self, input_password: str, hashed_password: str) -> bool:
        ...
