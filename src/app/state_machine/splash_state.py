"""
Splash screen state, where the user can either sign in or sign up.
"""
from src.app.state import State, StatesEnum
from src.app.views.splash_view import SplashView

class SplashState(State):
    """
    Splash screen state, where the user can either sign in or sign up.
    """
    def __init__(self, context):
        super().__init__(context)

        # set the view
        self.view = SplashView(self.context.ui.root)
        # update the view in the ui
        self.context.ui.view = self.view

    def render(self):
        print("Rendering splash (sign in/up) page...")
        self.view.show()

        # bind events
        self.view.login_button.bind("<Button-1>", self.login)
        self.view.sign_up_button.bind("<Button-1>", self.sign_up)

    def login(self, _event):
        """
        Handle login button click.
        """
        self.transition_to(StatesEnum.LOGIN)

    def sign_up(self, _event):
        """
        Handle sign up button click.
        """
        self.transition_to(StatesEnum.SIGNUP)
