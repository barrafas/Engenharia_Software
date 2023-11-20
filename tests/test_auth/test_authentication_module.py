import unittest
from src.auth.authentication import Authentication
from src.database.text_document_module import TextDocumentModule
from src.auth.user_management import UserManagement

class TestAuthenticationModule(unittest.TestCase):
    def setUp(self):
        # Set up for the tests
        self.database_module_mock = TextDocumentModule("tests/test_auth/test_database.json")
        self.database_module_mock.clear_data()
        self.auth_module = Authentication(self.database_module_mock)
        self.user_management_module = UserManagement(self.database_module_mock)

        # Create a test user
        self.user_management_module.create_user(username="test_user", email="test_email", password="test_password")

    def test_successful_authentication(self):
        # Test successful authentication
        result = self.auth_module.authenticate_user("test_user", "test_password")
        self.assertTrue(result)

    def test_failed_authentication(self):
        # Test failed authentication
        result = self.auth_module.authenticate_user("test_user", "wrong_password")
        self.assertFalse(result)

    def test_logout_user(self):
        # Test user logout
        result = self.auth_module.logout_user("test_user")
        self.assertTrue(result)

    def tearDown(self):
        # Clean up after the tests
        self.database_module_mock.clear_data()

if __name__ == '__main__':
    unittest.main()
