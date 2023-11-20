import unittest
from src.auth.authentication import Authentication
from src.auth.user_management import UserManagement

class TestAuthenticationModule(unittest.TestCase):
    def setUp(self):
        # Set up for the tests
        self.auth_module = Authentication()
        self.user_management_module = UserManagement()

        # Create a test user
        self.user_management_module.create_user("test_user", "test_password")

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

if __name__ == '__main__':
    unittest.main()
