from src.auth.user_management import UserManagement
from src.database.text_document_module import TextDocumentModule
import bcrypt

class Authentication:
    def __init__(self, database_module):
        # Inicializar o módulo de autenticação
        self.database_module = database_module
        self.user_management_module = UserManagement(self.database_module)

    def authenticate_user(self, username, password):
        # Autenticar o usuário
        user_info = self.user_management_module.get_user(username)

        if user_info and self.verify_password(password, user_info['password']):
            print("\033[32m[SUCESSO]\033[0m Autenticação bem-sucedida para o usuário:", username)
            return True
        else:
            print("\033[31m[ERRO]\033[0m Falha na autenticação para o usuário:", username)
            return False

    def verify_password(self, input_password, hashed_password):
        # Verificar a senha fornecida com a senha armazenada
        return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def logout_user(self, username):
        # Sair do usuário
        print("\033[32m[SUCESSO]\033[0m Usuário desconectado:", username)
        return True
