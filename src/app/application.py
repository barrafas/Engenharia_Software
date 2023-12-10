"""
The Application defines the interface of interest to clients.
"""

from __future__ import annotations
from src.user.user_management import UserManagement
from src.auth.authentication import AuthenticationModule

class Application:
    """
    The Application defines the interface of interest to clients.
    """
    _state = None

    def __init__(self, state = None, ui = None, db = None) -> None:
        if state is not None:
            self.transition_to(state)
        self._ui = ui
        self._db = db


    def transition_to(self, state) -> None:
        """
        The Application allows changing the State object at runtime.
        """
        if self._state is not None:
            self._state.clear()
        print(f"Application: Transition to {type(state).__name__}")
        self._state = state
        self._state.context = self
        state.render()


    def run(self) -> None:
        """
        The Application delegates part of its behavior to the current State
        object.
        """
        self._ui.run()

    def close(self) -> None:
        """
        The Application delegates part of its behavior to the current State
        object.
        """

    def login(self, username, password):
        """
        The Application delegates part of its behavior to the current State
        object.
        """
        auth = AuthenticationModule(self._db)

        if auth.authenticate_user(username, password):
            print(f"\033[92mUser {username} authenticated.\033[0m")
            return True
        else:
            print("Login failed.")

    def sign_up(self, username, email, password):
        """
        The Application delegates part of its behavior to the current State
        object.
        """
        user_management = UserManagement(self._db)

        if user_management.create_user(username, email, password, id=username):
            print(f"\033[92mSign up successful! User {username} created.\033[0m")
            return True
        else:
            print("Sign up failed.")