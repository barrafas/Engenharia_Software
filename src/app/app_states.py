from src.app.state import State
import datetime


class MainState(State):
    def __init__(self, context):
        self.context = context
        self.events = {}

        self.events = self.context.get_user_events()
        
    def login(self):
        print("You are already logged in.")

    def logout(self, event):
        print("Logging out...")
        self.context.user = None
        self.context.transition_to(SignInUp(self.context))

    def render(self):
        print("Rendering main page...")

        # show main elements
        self.context._ui.show_main_elements(self.events)


        # bind events
        self.context._ui.logout_button.bind("<Button-1>", self.logout)
        self.context._ui.go_back_button.bind("<Button-1>", self.go_back)


        print("Binding calendar events...")
        # bind calendar events
        for day, button in self.context._ui.calendar_days.items():
            args = day
            button.bind("<Button-1>", lambda event, args=args: self.show_day_events(event, args))

    def show_day_events(self, event, args):
        # transition to day events state
        day = args
        self.context.transition_to(DayEventsState(self.context, day))

    def clear(self):
        self.context._ui.clear_elements()

    def go_back(self, event):
        # transition to sign-in/up state
        self.context.user = None
        self.context.transition_to(LoggedOut(self.context))

    def __str__(self):
        return "Main State"
        

class SignUpState(State):
    def __init__(self, context):
        self.context = context

    def login(self):
        print("You need to sign up first.")

    def logout(self):
        print("You are already logged out.")

    def render(self):
        print("Rendering sign up page...")
        self.context._ui.show_sign_up_elements()

        # bind events
        self.context._ui.sign_up_button.bind("<Button-1>", self.sign_up)
        self.context._ui.go_back_button.bind("<Button-1>", self.go_back)
        
        # binding the enter press on the password entry to the login function
        self.context._ui.password_entry.bind("<Return>", self.sign_up)

    def clear(self):
        self.context._ui.clear_elements()

    def go_back(self, event):
        # transition to sign-in/up state
        self.context.transition_to(SignInUp(self.context))
    
    def sign_up(self, event):
        user_id = self.context._ui.user_id_entry.get()
        username = self.context._ui.username_entry.get()
        email = self.context._ui.email_entry.get()
        password = self.context._ui.password_entry.get()

        print("Signing up...")
        if self.context.sign_up(user_id, username, email, password):
            # transition to main state
            self.context.transition_to(LoggedOut(self.context))

class DayEventsState(State):
    def __init__(self, context, day):
        self.context = context
        self.events = {}
        self.day = day

        self.events = self.context.get_user_events()
        self.day_events = self.events.get(day[0], {}).get(day[1], {}).get(day[2], [])
        
    def login(self):
        print("You are already logged in.")

    def logout(self, event):
        print("Logging out...")
        self.context.user = None
        self.context.transition_to(SignInUp(self.context))

    def create_event(self, event):
        year, month, day = self.day
        selected_date = datetime.date(year, month, day)

        event_name = self.context._ui.event_name_entry.get()
        event_type = self.context._ui.event_type_selector.get()

        print(f"[\033[92m <> \033[0m] Event name: {event_name}, Event type: {event_type}, Event date: {selected_date}")

        print("Creating event...")
        print(f"Event name: {event_name}")
        print(f"Event type: {event_type}")
        print(f"Event date: {selected_date}")

        self.context.create_event(event_name, event_type, selected_date)

  

    def render(self):
        print("Rendering main page...")

        # show the day events
        self.context._ui.show_day_events(self.day_events, self.day)

        # bind events
        self.context._ui.logout_button.bind("<Button-1>", self.logout)
        self.context._ui.go_back_button.bind("<Button-1>", self.go_back)
        self.context._ui.create_event_button.bind("<Button-1>", self.create_event)

    def clear(self):
        self.context._ui.clear_elements()

    def go_back(self, event):
        # transition to the main state
        self.context.transition_to(MainState(self.context))

    def __str__(self):
        return "Events State"