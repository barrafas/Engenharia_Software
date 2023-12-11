"""
Test the authentication module
"""
import unittest
from unittest.mock import MagicMock
import bcrypt
from src.auth.authentication import AuthenticationModule, UserNotFound

class TestAuthenticationModule(unittest.TestCase):
    """
    Class to test the authentication module

    Methods:
        setUp
        test_authenticate_user_success
        test_authenticate_user_wrong_password
        test_authenticate_user_user_not_found
        test_password_verification_success
        test_password_verification_failure
        create_mock_user
    """
    def setUp(self):
        """ Function that runs before each test case """
        from src.user.user_management import UserManagement
        self.database_module_mock = MagicMock()
        UserManagement.get_instance(self.database_module_mock)
        self.auth_module = AuthenticationModule()

    def test_authenticate_user_success(self):
        """ Test the authenticate_user method success case """
        self.auth_module.user_management_module.user_exists = MagicMock(\
            return_value=True)
        self.auth_module.user_management_module.get_user = MagicMock(\
            return_value=self.create_mock_user())

        # Mocking verify_password method
        self.auth_module.verify_password = MagicMock(return_value=True)

        result = self.auth_module.authenticate_user("test_user",
                                                    "test_password")
        self.assertTrue(result)

    def test_authenticate_user_wrong_password(self):
        """ Test the authenticate_user method wrong password case """
        self.auth_module.user_management_module.user_exists = MagicMock(
            return_value=True)
        self.auth_module.user_management_module.get_user = MagicMock(
            return_value=self.create_mock_user())

        # Mocking verify_password method
        self.auth_module.verify_password = MagicMock(return_value=False)

        result = self.auth_module.authenticate_user("test_user",
                                                    "wrong_password")
        self.assertFalse(result)

    def test_password_verification_success(self):
        """ Test the verify_password method success case """
        bcrypt.checkpw = MagicMock(return_value=True)

        result = self.auth_module.verify_password("test_password",
                                                  "test_hashed_password")
        self.assertTrue(result)

    def test_password_verification_failure(self):
        """ Test the verify_password method failure case """
        bcrypt.checkpw = MagicMock(return_value=False)

        result = self.auth_module.verify_password("test_password",
                                                  "test_hashed_password")
        self.assertFalse(result)

    def test_authenticate_user_user_not_found(self):
        """ Test the authenticate_user method user not found case """
        self.auth_module.user_management_module.user_exists = MagicMock(\
            return_value=False)

        with self.assertRaises(UserNotFound):
            self.auth_module.authenticate_user("nonexistent_user", "password")

    def create_mock_user(self):
        """ Create a mock user """
        user = MagicMock()
        hash_t = b'$2b$12$4PVzqGrnWdUzWd9s/VoI2u6cfTS58zvVqEzUzTijp8usZbRAnkE/W'
        user.get_hashed_password = MagicMock(return_value=hash_t)
        return user

if __name__ == '__main__': # pragma: no cover
    unittest.main() # pragma: no cover
