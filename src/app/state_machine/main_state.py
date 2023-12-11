"""
Main state is the state that shows the user's calendar.
"""
from src.app.state import State, StatesEnum
from src.app.views.main_view import MainView

class MainState(State):
    """
    Main state is the state that shows the user's calendar.
    """
    def __init__(self, context):
        super().__init__(context)

        if not self.logged_in_user():
            # transition to splash state
            self.transition_to(StatesEnum.SPLASH)

        self.events = {}
        self.events = self.context.get_user_events()

        # set the view
        self.view = MainView(self.context.ui.root, self.events)
        # update the view in the ui
        self.context.ui.view = self.view

    def logged_in_user(self):
        """
        Get the logged in user.
        """
        return self.context.user

    def render(self):
        print("Rendering main page...")
        self.view.show()

        # bind events
        self.view.logout_button.bind("<Button-1>", self.logout)
        self.view.go_back_button.bind("<Button-1>", self.go_back)

        # bind calendar buttons
        for day, button in self.view.calendar_buttons_tree.items():
            button.bind("<Button-1>", lambda event, args=day: self.show_day_events(event, args))

    def logout(self, _event):
        """
        Handle logout button click.
        """
        self.transition_to(StatesEnum.LOGGOUT)

    def go_back(self, _event):
        """
        Handle go back button click.
        """
        self.transition_to(StatesEnum.LOGGOUT)

    def show_day_events(self, _event, args):
        """
        Handle day button click.
        """
        day = args
        self.transition_to(StatesEnum.DAYEVENTS, day=day)

    def __str__(self):
        return "Main State"
