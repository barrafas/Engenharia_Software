"""
Main state is the state that shows the user's calendar.
"""
from src.app.state import State, StatesEnum
from src.app.views.main_view import MainView
import datetime

class MainState(State):
    """
    Main state is the state that shows the user's calendar.
    """
    def __init__(self, context):
        super().__init__(context)

        if not self.logged_in_user():
            # transition to splash state
            self.transition_to(StatesEnum.SPLASH)

        self.events_tree = self.context.get_user_events()

        # set the view
        self.view = MainView(self.context.ui.root, self.events_tree)
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

        # bind calendar buttons, each key of the tree is the (year, month, day) tuple
        for yy_mm_dd, button in self.view.calendar_buttons.items():
            button.bind("<Button-1>", lambda event, args=yy_mm_dd: self.show_day_events(event, args))

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

    def show_day_events(self, _event, selected_date):
        """
        Handle day button click.
        """
        year = selected_date[0]
        month = selected_date[1]
        day = selected_date[2]

        selected_day = datetime.date(year, month, day)
        day_events = self.events_tree.get(year, {}).get(month, {}).get(day, {})

        self.transition_to(StatesEnum.DAYEVENTS, day_events=day_events, selected_day=selected_day)

    def __str__(self):
        return "Main State"
