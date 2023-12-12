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

        self.view.database_url_entry = str(self.context._db.host) if self.context._db else "localhost"
        self.view.database_port_entry = str(self.context._db.port) if self.context._db else "27017"
        self.view.database_user_entry = str(self.context._db.user) if self.context._db else ""
        self.view.database_password_entry = str(self.context._db.password) if self.context._db else ""

    def render(self):
        self.view.show()

        # bind events
        self.view.login_button.bind("<Button-1>", self.login)
        self.view.sign_up_button.bind("<Button-1>", self.sign_up)

    def login(self, _event):
        """
        Handle login button click.
        """
        self.set_database()
        self.transition_to(StatesEnum.LOGIN)

    def sign_up(self, _event):
        """
        Handle sign up button click.
        """
        self.set_database()
        self.transition_to(StatesEnum.SIGNUP)

    def set_database(self):
        """
        Set the database.
        """
        # get the database config
        database_url = self.view.database_url_entry.get()
        database_port = self.view.database_port_entry.get()
        database_user = self.view.database_user_entry.get()
        database_password = self.view.database_password_entry.get()

        # set the database config
        self.context.initialize_database(database_url, database_port, database_user,
            database_password)