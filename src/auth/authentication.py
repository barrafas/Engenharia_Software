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
        if not self.user_management_module.user_exists(username):
            print("\033[31m[ERRO]\033[0m Usuário não encontrado:", username)
            return False
        else:
            user = self.user_management_module.get_user(username)
            user_password = user.get_hashed_password() if user else None

            if self.verify_password(password, user_password):
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
