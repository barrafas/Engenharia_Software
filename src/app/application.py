"""
The Application defines the interface of interest to clients.
"""

from __future__ import annotations

import random
from src.user.user_management import UserManagement
from src.calendar_elements.element_management import ElementManagement
from src.schedule.schedule_management import ScheduleManagement
from src.auth.authentication import AuthenticationModule
from src.database.mongo_module import MongoModule
from src.database.utils import TimeoutDecorator

class Application:
    """
    The Application defines the interface of interest to clients.
    """
    _state = None

    def __init__(self, state = None, ui = None, db = None) -> None:
        self._state = state
        self._ui = ui
        self._db = db
        self._user = None
        self.selected_schedules = []

    def initialize_database(self, database_url, database_port, database_user, database_password):
        """
        Initialize the database
        """
        if database_user == "None" or database_password == "":
            database_user = None
            database_password = None
        if database_password == "None" or database_password == "":
            database_password = None
        database_port = int(database_port)
        MongoModule._instance = None
        user = {}
        if database_user:
            user = {"user": database_user, "password": database_password}
        self._db = TimeoutDecorator(
                    MongoModule(host = database_url,
                        port = database_port,
                        database_name = "calendar_app",
                        **user)
                    , 5)

        self._db.connect()
        print(f"\033[92mDatabase initialized: {self._db}\033[0m")

        self.initialize_managers()

    def initialize_managers(self):
        """
        Initialize the managers
        """
        # initialize modules
        ScheduleManagement._instance = None
        ElementManagement._instance = None
        UserManagement._instance = None
        ScheduleManagement.get_instance(database_module=self._db)
        ElementManagement.get_instance(database_module=self._db)
        UserManagement.get_instance(database_module=self._db)

    def transition_to(self, state) -> None:
        """
        The Application allows changing the State object at runtime.
        """
        if self._state is not None:
            self._state.clear()
        print(f"Application: Transition to {type(state).__name__}")
        self._state = state
        state.render()

    @property
    def db(self):
        return self._db
    
    @db.setter
    def db(self, db):
        self._db = db
        self.initialize_managers()

    @property
    def state(self):
        return self._state
    
    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, user):
        self._user = user
        if user:
            self.selected_schedules = user.schedules
        else:
            self.selected_schedules = []

    @property
    def ui(self):
        return self._ui

    @ui.setter
    def ui(self, ui):
        self._ui = ui

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
        auth = AuthenticationModule()

        if auth.authenticate_user(user_id, password):
            print(f"\033[92mUser {user_id} authenticated.\033[0m")
            self.user = UserManagement(self._db).get_user(user_id)
            return True
        else:
            print("Login failed.")

    def logout(self):
        """
        The Application delegates part of its behavior to the current State
        object.
        """
        self.user = None

    def sign_up(self, user_id, username, email, password):
        """
        The Application delegates part of its behavior to the current State
        object.
        """
        user_management = UserManagement.get_instance()

        user = user_management.create_user(username, email, password, user_id=user_id)

        if user:
            print(f"\033[92mSign up successful! User {username} created.\033[0m")

            schedule_management = ScheduleManagement.get_instance()
            schedule_id = f"{user_id}_schedule"
            schedule_title = "Private schedule"
            schedule_description = f"Private schedule of {username}"
            schedule_permissions = {user_id: "owner"}
            schedule = schedule_management.create_schedule(schedule_id, schedule_title,
                                        schedule_description, schedule_permissions, [])

            print(f"\033[92mSchedule created: {schedule}\033[0m")
            print(f"\033[92mUser schedules: {user.schedules}\033[0m")

            self.login(user_id, password)

            return True
        else:
            print("Sign up failed.")

    def get_user_events(self):
        """
        Return the user's events as a dictionary in the tree format:
        {
            year: {
                month: {
                    day: {
                        hour: {
                            minute: [event1, event2, ...]
                        }
                    }
                }
            }
        }

        """
        elements = self.user.get_elements(self.selected_schedules)

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

        return elements

    def create_event(self, element_type: str, title: str,
                       schedules: list, **kwargs):
        """
        The Application delegates part of its behavior to the current State
        object.
        """
        element_id = self.user.id + "_" + title + str(random.randint(0, 1000))
        element_management = ElementManagement.get_instance()
        event = element_management.create_element(element_type = element_type,
            element_id = element_id, title = title, schedules = schedules, **kwargs)

        print(f"\033[92mEvent created: {event}\033[0m")
        return event

    def delete_element(self, element):
        """
        Deleting a element
        """
        element_management = ElementManagement.get_instance()
        element_management.delete_element(element.id)