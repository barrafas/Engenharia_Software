"""
State for user account creation.
"""
from src.app.state import State, StatesEnum
from src.app.views.sign_up_view import SignUpView

class SignUpState(State):
    def __init__(self, context):
        super().__init__(context)

        # check if the user is already logged in
        if self.context.user:
            print("User is already logged in.")
            # transition to main state
            self.transition_to(StatesEnum.MAIN)

        # set the view
        self.view = SignUpView(self.context.ui.root)
        # update the view in the ui
        self.context.ui.view = self.view

    def render(self):
        print("Rendering sign up page...")
        self.view.show()

        # bind events
        self.view.sign_up_button.bind("<Button-1>", self.sign_up)
        self.view.go_back_button.bind("<Button-1>", self.go_back)

        # binding the enter press on the password entry to the login function
        self.view.password_entry.bind("<Return>", self.sign_up)

    def sign_up(self, _event):
        """
        Handle sign up button click.
        """
        user_id = self.view.user_id_entry.get()
        username = self.view.user_id_entry.get()
        email = self.view.email_entry.get()
        password = self.view.password_entry.get()

        print("Signing up...")
        if self.context.sign_up(user_id, username, email, password):
            # transition to main state
            self.transition_to(StatesEnum.MAIN)

    def go_back(self, _event):
        """
        Handle go back button click.
        """
        self.transition_to(StatesEnum.SPLASH)
