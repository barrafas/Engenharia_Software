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
        self._user = None


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

    def login(self, user_id, password):
        """
        The Application delegates part of its behavior to the current State
        object.
        """
        auth = AuthenticationModule(self._db)

        if auth.authenticate_user(user_id, password):
            print(f"\033[92mUser {user_id} authenticated.\033[0m")
            self._user = UserManagement(self._db).get_user(user_id)
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

    def get_user_events(self):
        """
        The Application delegates part of its behavior to the current State
        object.
        """
        elements = self._user.events

        """
        Gets the events from the user and stores them in a dictionary
        """
        # get user events
        events = elements
        elements = {}

        for event in events:
            date = event.get_display_interval()[0]

            yearly_events = elements.get(date.year, {})
            monthly_events = yearly_events.get(date.month, {})
            daily_events = monthly_events.get(date.day, {})
            hourly_events = daily_events.get(date.hour, {})
            minutely_events = hourly_events.get(date.minute, [])

            minutely_events.append(event)

            hourly_events[date.minute] = minutely_events
            daily_events[date.hour] = hourly_events
            monthly_events[date.day] = daily_events
            yearly_events[date.month] = monthly_events

            elements[date.year] = yearly_events


        print(f"\033[92mUser events: {elements}, with len ={len(elements)}\033[0m")

        event_titles = []
        for event in elements:
            event_titles.append(event.title)

        return event_titles
        
