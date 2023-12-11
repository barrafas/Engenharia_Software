"""
State that shows and manage the user's events for a specific day.
"""
from src.app.state import State, StatesEnum
from src.app.views.day_events_view import DayEventsView

class DayEventsState(State):
    """
    State that shows and manage the user's events for a specific day.
    """
    def __init__(self, context, day_events, selected_day):
        super().__init__(context)

        if not self.logged_in_user():
            # transition to splash state
            self.transition_to(StatesEnum.SPLASH)

        self.day_events = day_events
        self.selected_day = selected_day

        # set the view
        self.view = DayEventsView(self.context.ui.root, self.day_events, self.selected_day)
        # update the view in the ui
        self.context.ui.view = self.view

    def logged_in_user(self):
        """
        Get the logged in user.
        """
        return self.context.user

    def render(self):
        print("Rendering day events page...")
        self.view.show()

        # bind events
        self.view.go_back_button.bind("<Button-1>", self.go_back)
        self.view.create_event_button.bind("<Button-1>", self.create_event)

        self.bind_hour_buttons()

    def bind_hour_buttons(self):
        """
        Bind the hour buttons.
        """
        for key, hour_frame in self.view.hour_buttons.items():
            hour_frame.bind("<Button-1>", self.hour_button_click)
            # adding a hover effect to the hour frame
            color = hour_frame._fg_color
            hover_color = "gray"
            hour_frame.bind("<Enter>", lambda event, frame=hour_frame, hover_color=hover_color: frame.configure(fg_color=hover_color))
            hour_frame.bind("<Leave>", lambda event, frame=hour_frame, color=color: frame.configure(fg_color=color))

    def bind_event_buttons(self):
        """
        Bind the event buttons.
        """
        for event_button in self.view.event_buttons:
            event_button.bind("<Button-1>", self.event_button_click)

    def event_button_click(self, event):
        """
        Handle event button click.
        """

    def hour_button_click(self, event):
        """
        Handle hour button click.
        """

    def logout(self, _event):
        """
        Handle logout button click.
        """
        self.transition_to(StatesEnum.LOGGOUT)

    def go_back(self, _event):
        """
        Handle go back button click.
        """
        self.transition_to(StatesEnum.MAIN)

    def create_event(self, _event):
        """
        Handle create event button click.
        """
        event_name = self.view.event_name_entry.get()
        event_type = self.view.event_type_selector.get()

        print(event_name)
        print(event_type)

        self.context.create_event(event_name, event_type, self.selected_day)

        self.transition_to(StatesEnum.MAIN)
