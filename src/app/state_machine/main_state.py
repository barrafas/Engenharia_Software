"""
Main state is the state that shows the user's calendar.
"""
import datetime

from src.app.views.main_view import MainView
from src.app.state import State, StatesEnum

class MainState(State):
    """
    Main state is the state that shows the user's calendar.
    """
    def __init__(self, context, month = None, year = None):
        super().__init__(context)

        if month is None:
            month = datetime.date.today().month

        if year is None:
            year = datetime.date.today().year

        if not self.logged_in_user():
            # transition to splash state
            self.transition_to(StatesEnum.SPLASH)

        self.events_tree = self.context.get_user_events()

        self.selected_month = month
        self.selected_year = year

        # set the view
        self.view = MainView(self.context.ui.root, self.events_tree)
        # update the view in the ui
        self.context.ui.view = self.view

        self.view.logged_user_name = self.logged_in_user().username

    def logged_in_user(self):
        """
        Get the logged in user.
        """
        return self.context.user

    def render(self):
        self.view.selected_date = datetime.date(self.selected_year, self.selected_month, 1)
        self.view.show()

        # bind events
        self.view.logout_button.bind("<Button-1>", self.logout)
        self.view.go_back_button.bind("<Button-1>", self.go_back)

        self.view.next_month_button.bind("<Button-1>", self.go_next_month)
        self.view.prev_month_button.bind("<Button-1>", self.go_prev_month)

        self.view.export_data_button.bind("<Button-1>", self.export_data)

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

    def go_next_month(self, _event):
        """
        Handle next month button click.
        """
        if self.selected_month == 12:
            self.selected_month = 1
            self.selected_year += 1
        else:
            self.selected_month += 1

        self.transition_to(StatesEnum.MAIN, month=self.selected_month, year=self.selected_year)

    def go_prev_month(self, _event):
        """
        Handle previous month button click.
        """
        if self.selected_month == 1:
            self.selected_month = 12
            self.selected_year -= 1
        else:
            self.selected_month -= 1

        self.transition_to(StatesEnum.MAIN, month=self.selected_month, year=self.selected_year)

    def export_data(self, _event):
        """
        Handle export data button click.
        """
        self.context.export_data()

    def __str__(self):
        return "Main State"
