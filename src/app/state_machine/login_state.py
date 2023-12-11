from src.app.state import State, StatesEnum
from src.app.views.login_view import LoginView

class LoginState(State):
    def __init__(self, context):
        super().__init__(context)

        # set the view
        self.view = LoginView(self.context.ui.root)
        # update the view in the ui
        self.context.ui.view = self.view

    def render(self):
        print("Rendering logged out page...")
        self.view.show()

        # bind events
        self.view.login_button.bind("<Button-1>", self.login)
        self.view.go_back_button.bind("<Button-1>", self.go_back)

        # binding the enter press on the password entry to the login function
        self.view.password_entry.bind("<Return>", self.login)


    def login(self, _event):
        """
        Handle login button click.
        """
        username = self.view.user_id_entry.get()
        password = self.view.password_entry.get()

        print("Logging in...")
        if self.context.login(username, password):
            # transition to main state
            self.transition_to(StatesEnum.MAIN)
    
    def go_back(self, _event):
        """
        Handle go back button click.
        """
        self.transition_to(StatesEnum.SPLASH)

    def __str__(self):
        return "Logged Out"

