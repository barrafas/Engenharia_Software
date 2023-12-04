"""
Test the authentication module

TODO:
    - Review the tests
    - Review the documentation
"""
import unittest
from src.auth.authentication import Authentication
from src.database.text_document_module import TextDocumentModule
from src.auth.user_management import UserManagement


class TestAuthenticationModule(unittest.TestCase):
    """_summary_

    Arguments:
        unittest -- _description_
    """

    def setUp(self):
        """
        Set up the test environment
        """
        self.database_module_mock = TextDocumentModule(
            "tests/test_auth/test_database.json")
        self.database_module_mock.clear_data()
        self.auth_module = Authentication(self.database_module_mock)
        self.user_management_module = UserManagement(self.database_module_mock)

        # Create a test user
        self.user_management_module.create_user(username="test_user",
                                                email="test_email", password="test_password")

    def test_successful_authentication(self):
        """
        GIVEN a user that exists in the database
        WHEN the user tries to authenticate with the correct password
        THEN the authentication should be successful
        """
        result = self.auth_module.authenticate_user(
            "test_user", "test_password")
        self.assertTrue(result)

    def test_failed_authentication(self):
        """
        GIVEN a user that exists in the database
        WHEN the user tries to authenticate with the wrong password
        THEN the authentication should fail
        """
        result = self.auth_module.authenticate_user(
            "test_user", "wrong_password")
        self.assertFalse(result)

    def test_logout_user(self):
        """
        GIVEN a user that is logged in
        WHEN the user tries to logout
        THEN the user should be logged out
        """
        self.auth_module.authenticate_user("test_user", "test_password")
        self.auth_module.logout_user("test_user")


    def tearDown(self):
        """
        Clean up after the tests, resets the database
        """
        self.database_module_mock.clear_data()


if __name__ == '__main__':
    unittest.main() # pragma: no cover
