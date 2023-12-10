
"""
Test the authentication module

TODO:
    - Review the tests
    - Review the documentation
"""
import unittest
from unittest.mock import MagicMock
from src.auth.authentication import AuthenticationModule
import bcrypt

class TestAuthenticationModule(unittest.TestCase):
    def setUp(self):
        # You may want to mock the database module for testing
        self.database_module_mock = MagicMock()
        self.auth_module = AuthenticationModule(self.database_module_mock)

    def test_authenticate_user_success(self):
        # Mocking user_exists and get_user methods
        self.auth_module.user_management_module.user_exists = MagicMock(return_value=True)
        self.auth_module.user_management_module.get_user = MagicMock(return_value=self.create_mock_user())

        # Mocking verify_password method
        self.auth_module.verify_password = MagicMock(return_value=True)

        # Test
        result = self.auth_module.authenticate_user("test_user", "test_password")
        self.assertTrue(result)

    def test_authenticate_user_wrong_password(self):
        # Mocking user_exists and get_user methods
        self.auth_module.user_management_module.user_exists = MagicMock(return_value=True)
        self.auth_module.user_management_module.get_user = MagicMock(return_value=self.create_mock_user())

        # Mocking verify_password method
        self.auth_module.verify_password = MagicMock(return_value=False)

        # Test
        result = self.auth_module.authenticate_user("test_user", "wrong_password")
        self.assertFalse(result)

    def test_password_verification_success(self):
        # Mocking bcrypt.checkpw method
        bcrypt.checkpw = MagicMock(return_value=True)

        # Test
        result = self.auth_module.verify_password("test_password", "test_hashed_password")
        self.assertTrue(result)

    def test_password_verification_failure(self):
        # Mocking bcrypt.checkpw method
        bcrypt.checkpw = MagicMock(return_value=False)

        # Test
        result = self.auth_module.verify_password("test_password", "test_hashed_password")
        self.assertFalse(result)

    def create_mock_user(self):
        # You may want to create a mock user for testing purposes
        user = MagicMock()
        user.get_hashed_password = MagicMock(return_value=b'$2b$12$4PVzqGrnWdUzWd9s/VoI2u6cfTS58zvVqEzUzTijp8usZbRAnkE/W')
        return user

if __name__ == '__main__':
    unittest.main()
