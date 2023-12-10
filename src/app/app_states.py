from src.app.state import State

class SignInUp(State):
    def __init__(self, context):
        self.context = context

    def render(self):
        print("Rendering sign in/up page...")
        self.context._ui.show_sign_in_up_elements()

        # bind events
        self.context._ui.login_button.bind("<Button-1>", self.login)
        self.context._ui.sign_up_button.bind("<Button-1>", self.sign_up)


    def clear(self):
        self.context._ui.clear_elements()

    def go_back(self):
        print("You are already in the sign in/up page.")

    def logout(self):
        print("You are already logged out.")

    def login(self, event):
        # transition to logged out state
        self.context.transition_to(LoggedOut(self.context))

    def sign_up(self, event):
        # transition to logged out state
        self.context.transition_to(SignUpState(self.context))


class LoggedOut(State):
    def __init__(self, context):
        self.context = context

    def login(self, event):

        username = self.context._ui.user_id_entry.get()
        password = self.context._ui.password_entry.get()

        print("Logging in...")
        if self.context.login(username, password):
            # transition to main state
            self.context.transition_to(MainState(self.context))

    def logout(self):
        print("You are already logged out.")

    def render(self):
        print("Rendering logged out page...")
        self.context._ui.show_login_elements()

        # bind events
        self.context._ui.login_button.bind("<Button-1>", self.login)
        self.context._ui.go_back_button.bind("<Button-1>", self.go_back)

        # binding the enter press on the password entry to the login function
        self.context._ui.password_entry.bind("<Return>", self.login)

    def clear(self):
        self.context._ui.clear_elements()

    def go_back(self, event):
        # transition to sign-in/up state
        self.context.transition_to(SignInUp(self.context))

    def __str__(self):
        return "Logged Out"


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
        username = self.context._ui.user_id_entry.get()
        email = self.context._ui.email_entry.get()
        password = self.context._ui.password_entry.get()

        print("Signing up...")
        if self.context.sign_up(username, email, password):
            # transition to main state
            self.context.transition_to(LoggedOut(self.context))
