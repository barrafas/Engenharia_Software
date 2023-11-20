
import bcrypt
from src.database.database_module import DatabaseModule
from src.models.user_model import UserModel

INFO_STR = "\033[33m[INFO]\033[0m "

class UserManagement:
    def __init__(self, database_module: DatabaseModule):
        self.db = database_module
        self.db.connect()

    def create_user(self, username, email, password, user_id=None):
        if not self.user_exists(username):
            hashed_password = self.hash_password(password)
            hashed_password = hashed_password.decode('utf-8')

            if not user_id:
                user_id = self.db.get_next_id("users")

            user_info = {"user_id": user_id, "username": username, "email": email, "password": hashed_password, "events": []}
            self.db.execute_query({"entity": "users", "action": "insert", "data": user_info})

            print(INFO_STR+"Usuário criado com sucesso: ", user_info)
            return True
        else:
            raise Exception('Usuário já existe')

    def delete_user(self, username):
        if self.user_exists(username):
            self.db.execute_query({"entity": "users", "action": "delete", "criteria": {"username": username}})
            return True
        else:
            raise Exception('Usuário não encontrado')

    def user_exists(self, username):
        query = {"entity": "users", "criteria": {"username": username}}
        data = self.db.fetch_data(query)
        return len(data) > 0

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def save_user_info(self, user):
        self.db.execute_query({"entity": "users", "action": "update", "criteria": {"username": user.username}, "data": user.to_json()})

    def get_user(self, username):
        query = {"entity": "users", "criteria": {"username": username}}
        data = self.db.fetch_data(query)
        return UserModel.from_json(data[0]) if len(data) > 0 else None

    def add_event_to_user(self, username, event_id):
        user = self.get_user(username)

        if user:
            user.events.append(event_id)
            self.db.execute_query({"entity": "users", "action": "update", "criteria": {"username": username}, "data": user.to_json()})
            return True
        else:
            return False