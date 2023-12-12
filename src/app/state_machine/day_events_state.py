"""
State that shows and manage the user's events for a specific day.
"""
import datetime
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
        self.currently_selected_event = None

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
        self.bind_event_buttons()
        self.bind_create_event_button()
        self.bind_delete_event_button()
        self.bind_update_event_button()

    def bind_hour_buttons(self):
        """
        Bind the hour buttons.
        """
        for (hour, minute), hour_frame in self.view.hour_buttons.items():
            # adding a click event to the hour frame
            hour_frame.bind("<Button-1>", lambda event, frame=hour_frame, hour=hour, minute=minute: self.hour_button_click(event, hour, minute, frame))
            
            # adding a hover effect to the hour frame
            color = hour_frame._fg_color # pylint: disable=protected-access
            hover_color = "gray"
            hour_frame.bind("<Enter>", lambda event, frame=hour_frame, hover_color=hover_color: frame.configure(fg_color=hover_color))
            hour_frame.bind("<Leave>", lambda event, frame=hour_frame, color=color: frame.configure(fg_color=color))

    def bind_event_buttons(self):
        """
        Bind the event buttons.
        """
        for event_button in self.view.event_buttons:
            button = event_button["button"]
            element = event_button["event"]
            button.bind("<Button-1>", lambda event,
                element=element: self.event_button_click(event, element))

    def event_button_click(self, _event, element):
        """
        Handle event button click.
        """
        self.currently_selected_event = element
        self.view.currently_selected_event = element
        element_display = element.get_display_interval()[0]
        self.view.currently_selected_hour = element_display.hour
        self.view.currently_selected_minute = element_display.minute

        self.view.update_event_managing_elements()

    def hour_button_click(self, _event, hour, minute, hour_frame):
        """
        Handle hour button click.
        """

        # changing the color of the hour frame for a second
        fg_color = hour_frame._fg_color # pylint: disable=protected-access
        glow_color = "green"
        hour_frame.configure(fg_color=glow_color)
        self.view.root.after(300, lambda: hour_frame.configure(fg_color=fg_color))

        self.view.currently_selected_hour = int(hour)
        self.view.currently_selected_minute = int(minute)
        self.currently_selected_event = None
        self.view.currently_selected_event = None
        self.view.update_event_managing_elements()

        

    def bind_create_event_button(self):
        """
        Bind the create event button.
        """
        self.view.create_event_button.bind("<Button-1>", self.create_event)

    def bind_delete_event_button(self):
        """
        Bind the delete event button.
        """
        self.view.delete_event_button.bind("<Button-1>", self.delete_event)

    def bind_update_event_button(self):
        """
        Bind the update event button.
        """
        self.view.update_event_button.bind("<Button-1>", self.update_event)

    def create_event(self, _event):
        """
        Handle create event button click.
        """

        event_name = self.view.event_name_entry.get()
        event_type = self.view.event_type_selector.get()
        event_description = self.view.event_description_textbox.get("0.0", "end")
        event_hour = int(self.view.currently_selected_hour)
        event_minute = int(self.view.currently_selected_minute)
        year = self.selected_day.year
        month = self.selected_day.month
        day = self.selected_day.day

        selected_date = datetime.datetime(year, month, day, event_hour, event_minute)

        kwargs = {}
        if event_type == "task":
            kwargs["due_date"] = selected_date
            kwargs["state"] = "TODO"
        elif event_type == "reminder":
            kwargs["reminder_date"] = selected_date
        elif event_type == "event":
            kwargs["start"] = selected_date
            kwargs["end"] = datetime.datetime(selected_date.year,
            selected_date.month, selected_date.day, selected_date.hour,
            selected_date.minute) + datetime.timedelta(hours=1)
        kwargs["description"] = event_description

        selected_schedules = self.context.selected_schedules

        if self.context.create_event(event_type, title=event_name,
            schedules=selected_schedules, **kwargs):
            self.transition_to(StatesEnum.MAIN, month=month, year=year)

    def delete_event(self, _event):
        """
        Handle delete event button click.
        """
        if self.currently_selected_event:
            self.context.delete_element(self.currently_selected_event)
            self.transition_to(StatesEnum.MAIN, month=self.selected_day.month, year=self.selected_day.year)

    def update_event(self, _event):
        """
        Handle update event button click.
        """
        if self.currently_selected_event:
            event_name = self.view.event_name_entry.get()
            event_type = self.view.event_type_selector.get()
            event_description = self.view.event_description_textbox.get("0.0", "end")
            event_hour = int(self.view.currently_selected_hour)
            event_minute = int(self.view.currently_selected_minute)
            year = self.selected_day.year
            month = self.selected_day.month
            day = self.selected_day.day

            selected_date = datetime.datetime(year, month, day, event_hour, event_minute)

            kwargs = {}
            if event_type == "task":
                kwargs["due_date"] = selected_date
                kwargs["state"] = "TODO"
            elif event_type == "reminder":
                kwargs["reminder_date"] = selected_date
            elif event_type == "event":
                kwargs["start"] = selected_date
                kwargs["end"] = datetime.datetime(selected_date.year,
                selected_date.month, selected_date.day, selected_date.hour,
                selected_date.minute) + datetime.timedelta(hours=1)
            kwargs["description"] = event_description

            self.currently_selected_event.title = event_name
            self.currently_selected_event.description = event_description
            self.currently_selected_event.start = selected_date
            self.currently_selected_event.end = datetime.datetime(selected_date.year,
            selected_date.month, selected_date.day, selected_date.hour,
            selected_date.minute) + datetime.timedelta(hours=1)

            self.transition_to(StatesEnum.MAIN, month=month, year=year)

    def logout(self, _event):
        """
        Handle logout button click.
        """
        self.transition_to(StatesEnum.LOGGOUT)

    def go_back(self, _event):
        """
        Handle go back button click.
        """
        self.transition_to(StatesEnum.MAIN, month=self.selected_day.month, year=self.selected_day.year)
