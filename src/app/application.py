"""
The Application defines the interface of interest to clients.
"""

from __future__ import annotations
from src.user.user_management import UserManagement
from src.calendar_elements.element_management import ElementManagement
from src.schedule.schedule_management import ScheduleManagement
from src.auth.authentication import AuthenticationModule
import datetime

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
        auth = AuthenticationModule()

        if auth.authenticate_user(user_id, password):
            print(f"\033[92mUser {user_id} authenticated.\033[0m")
            self._user = UserManagement(self._db).get_user(user_id)
            return True
        else:
            print("Login failed.")

    def sign_up(self, user_id, username, email, password):
        """
        The Application delegates part of its behavior to the current State
        object.
        """
        user_management = UserManagement.get_instance()

        user = user_management.create_user(username, email, password, user_id=user_id)
        user.attach(user_management)

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

            return True
        else:
            print("Sign up failed.")

    def get_user_events(self):
        """
        The Application delegates part of its behavior to the current State
        object.
        
        Gets the events from the user and stores them in a dictionary

        """
        elements = self._user.get_elements()

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
        
    def create_event(self, event_name, event_type, selected_date):
        """
        The Application delegates part of its behavior to the current State
        object.
        """
        print(f"Schedules: {self._user.schedules}")
        schedule = self._user.schedules[0]
        print(f"Schedule: {schedule}")

        kwargs = {}
        if event_type == "Task":
            kwargs["due_date"] = selected_date
            kwargs["state"] = "TODO"
        elif event_type == "Reminder":
            kwargs["reminder_date"] = selected_date
        elif event_type == "Event":
            kwargs["start"] = selected_date
            kwargs["end"] = datetime.datetime(selected_date.year,
            selected_date.month, selected_date.day, selected_date.hour,
            selected_date.minute) + datetime.timedelta(hours=1)

        description = None

        element_management = ElementManagement.get_instance()
        event = element_management.create_element(element_type = event_type, element_id = event_name,
        title = event_name, description = description, schedules = [schedule.id], **kwargs)

        print(f"\033[92mEvent created: {event}\033[0m")
