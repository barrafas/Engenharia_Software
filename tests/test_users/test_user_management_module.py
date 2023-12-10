import unittest
from src.user.user_management import UserManagement
from unittest.mock import Mock, MagicMock, patch
import bcrypt

class TestUserManagementModule(unittest.TestCase):
    def setUp(self):
        # Set up for the tests
        UserManagement._instance = None
        # Cria um mock para a interface DatabaseModule
        self.db = Mock()
        self.user_management = UserManagement.get_instance(self.db)

    # def test_create_user_success(self):
    #     # Test creating a new user successfully
    #     result = self.user_management.create_user(
    #         username="test_user", email="test_email", password="test_password")
    #     self.assertEqual(result.username, "test_user")
    #     self.assertEqual(result.email, "test_email")
    #     self.assertTrue(bcrypt.checkpw("test_password".encode('utf-8'), 
    #                                    result.hashed_password))

    # def test_create_existing_user(self):
        # Test creating a user that already exists
        # self.user_management_module.create_user("existing_user", "existing_email", "existing_password")
        # with self.assertRaises(Exception) as context:
        #     self.user_management_module.create_user("existing_user", "existing_email", "existing_password")
        # self.assertEqual(str(context.exception), 'Usuário já existe')

    # def test_hash_password(self):
        # Test hashing a password
        # password = "test_password"
        # hashed_password = self.user_management_module.hash_password(password)
        # self.assertTrue(bcrypt.checkpw(password.encode('utf-8'), hashed_password))

    # def test_user_exists(self):
        # Test checking if a user exists
        # self.user_management_module.create_user("check_user", "check_email", "check_password")
        # result = self.user_management_module.user_exists("check_user")
        # self.assertTrue(result)

    # def test_user_not_exists(self):
    #     # Test checking if a user does not exist
    #     result = self.user_management_module.user_exists("nonexistent_user")
    #     self.assertFalse(result)

    # def test_delete_user(self):
    #     # Testa a exclusão de um usuário
    #     username = "user_to_delete"
    #     password = "password123"
    #     self.user_management_module.create_user(username, "delete_email@mail.com", password)

    #     # Verifica se o usuário existe antes da exclusão
    #     self.assertTrue(self.user_management_module.user_exists(username))

    #     # Exclui o usuário
    #     self.user_management_module.delete_user(username)

    #     # Verifica se o usuário não existe mais após a exclusão
    #     self.assertFalse(self.user_management_module.user_exists(username))

    # def tearDown(self):
    #     # Clean up after the tests
    #     self.database_module_mock.clear_data()

        
if __name__ == '__main__':
    unittest.main()
