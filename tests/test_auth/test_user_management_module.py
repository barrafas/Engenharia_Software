import unittest
from src.auth.user_management import UserManagement
from src.database.text_document_module import TextDocumentModule
import bcrypt

class TestUserManagementModule(unittest.TestCase):
    def setUp(self):
        # Set up for the tests

        # Cria um mock para a interface DatabaseModule
        self.database_module_mock = TextDocumentModule("tests/test_auth/test_database.json")

        # Inicializa a UserManagement com o mock da DatabaseModule
        self.user_management_module = UserManagement(self.database_module_mock)

    def test_create_user_success(self):
        # Test creating a new user successfully
        result = self.user_management_module.create_user("new_user", "new_password")
        self.assertTrue(result)

    def test_create_existing_user(self):
        # Test creating a user that already exists
        self.user_management_module.create_user("existing_user", "password123")
        with self.assertRaises(Exception) as context:
            self.user_management_module.create_user("existing_user", "new_password")
        self.assertEqual(str(context.exception), 'Usuário já existe')

    def test_hash_password(self):
        # Test hashing a password
        password = "test_password"
        hashed_password = self.user_management_module.hash_password(password)
        self.assertTrue(bcrypt.checkpw(password.encode('utf-8'), hashed_password))

    def test_user_exists(self):
        # Test checking if a user exists
        self.user_management_module.create_user("check_user", "check_password")
        result = self.user_management_module.user_exists("check_user")
        self.assertTrue(result)

    def test_user_not_exists(self):
        # Test checking if a user does not exist
        result = self.user_management_module.user_exists("nonexistent_user")
        self.assertFalse(result)

    def test_delete_user(self):
        # Testa a exclusão de um usuário
        username = "user_to_delete"
        password = "password123"
        self.user_management_module.create_user(username, password)

        # Verifica se o usuário existe antes da exclusão
        self.assertTrue(self.user_management_module.user_exists(username))

        # Exclui o usuário
        result = self.user_management_module.delete_user(username)
        self.assertTrue(result)

        # Verifica se o usuário não existe mais após a exclusão
        self.assertFalse(self.user_management_module.user_exists(username))

    def tearDown(self):
        # Clean up after the tests
        self.database_module_mock.clear_data()

        
if __name__ == '__main__':
    unittest.main()
