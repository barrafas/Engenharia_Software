"""
DayEventsView class, which is the view of the day events state.
"""
import customtkinter
from src.app.views.view import View
from typing import Mapping, Tuple, List
from src.calendar_elements.element_interface import Element

class DayEventsView(View):
    """
    DayEventsView class, which is the view of the day events state.

    It shows the user's events for a specific day and allows the user to create new events.

    args:
        root: A Tk root object, the root of the ui.
        day_events: A dict with the user's events for a specific day, in the format:
            {
                hour: {
                    minute: [event, event, ...],
                    minute: [event, event, ...],
                    ...
                },
                hour: {
                    minute: [event, event, ...],
                    minute: [event, event, ...],
                    ...
                },
                ...
            }
        selected_day: the selected day, in the format: (year, month, day)
    """
    def __init__(self, root, day_events: Mapping[int, Mapping[int, List[Element]]], selected_day: Tuple[int, int, int]):
        super().__init__(root)
        self.selected_day = selected_day

        self.go_back_button = None
        self.create_event_button = None
        self.event_name_entry = None
        self.event_type_selector = None

        self.day_events = day_events

        self.event_creation_frame = None
        self.today_events_frame = None

        self.hour_buttons = {}
        self.event_buttons = []

        self.event_types = ["task", "reminder", "event"]

    def show(self):
        # confuring the grid:
        # +----------+-----------------+
        # |  event   |                 |
        # | creation |     Today's     |
        # |          |     events      |
        # |          |                 |
        # +----------+-----------------+

        self.root.grid_columnconfigure((0), weight=1) # event creation
        self.root.grid_columnconfigure((1), weight=2) # today's events

        self.show_event_creation()
        self.show_today_events()

    def show_event_creation(self):
        self.event_creation_frame = customtkinter.CTkFrame(self.root)
        self.event_creation_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # event creation elements
        self.show_event_creation_elements()

    def show_event_creation_elements(self):
        self.go_back_button = customtkinter.CTkButton(self.event_creation_frame, text="Voltar")
        self.go_back_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.create_event_button = customtkinter.CTkButton(self.event_creation_frame, text="Criar evento")
        self.create_event_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.event_name_entry = customtkinter.CTkEntry(self.event_creation_frame)
        self.event_name_entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.event_type_selector = customtkinter.CTkOptionMenu(self.event_creation_frame, values=self.event_types)
        self.event_type_selector.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    def show_today_events(self):
        self.today_events_frame = customtkinter.CTkFrame(self.root)
        self.today_events_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # today's events elements
        self.show_today_events_elements()

    def show_today_events_elements(self):
        day_events_label = customtkinter.CTkLabel(self.today_events_frame, text=f"Eventos do dia {self.selected_day}")
        day_events_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.show_day_events()
    
    def show_day_events(self):
        self.day_events_list = customtkinter.CTkScrollableFrame(self.today_events_frame, width=400)
        self.day_events_list.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # day events elements
        self.show_day_events_elements(self.day_events)

    def show_day_events_elements(self, day_events: Mapping[int, Mapping[int, List[Element]]]):
        """
        Shows the day events elements
        """

        for hour in range(24):
            self.show_hour_events(hour, day_events.get(hour, {}))
            # hour_events = day_events.get(hour, {})

            # hour_label = customtkinter.CTkLabel(self.day_events_list, text=f"{hour}:00", **label_config)
            # hour_label.grid(row=hour*6, column=0, **padding_config, sticky="ew")

            # for minute, events in hour_events.items():
            #     clamp_minute = minute // 10 * 10
            #     minute_label = customtkinter.CTkLabel(self.day_events_list, text=f"{minute}", **label_config)
            #     minute_label.grid(row=hour*6+clamp_minute, column=1, **padding_config, sticky="ew")

            #     for event in events:
            #         event_label = customtkinter.CTkLabel(self.day_events_list, text=f"{event.title}", **label_config)
            #         event_label.grid(row=hour*6+clamp_minute, column=2, **padding_config, sticky="ew")

    def show_hour_events(self, hour: int, hour_events: Mapping[int, List[Element]]):
        label_config = {
            "height": 20,
            "width": 40
        }

        padding_config = {
            "padx": 8,
            "pady": 3
        }

        event_label_height = 10

        events_framming = {}
        for minute, events in hour_events.items():
            # clamping the minute to 0 or 30
            clamp_minute = minute // 30 * 30
            events_framming[clamp_minute] = events_framming.get(clamp_minute, []) + events

        for markings in [0, 1]:
            hour_frame = customtkinter.CTkFrame(self.day_events_list)
            hour_frame.pack(side="top", fill="both", expand=True, **padding_config)

            events = events_framming.get(markings*30, [])

            hour_label = customtkinter.CTkLabel(hour_frame, text=f"{hour:02d}:{markings*30:02d}", **label_config)
            hour_label.pack(side="left")

            for event in events:
                self.event_button(hour_frame, event)

            self.hour_buttons[(hour, markings*30)] = hour_frame
    
    def event_button(self, hour_frame, event):
        padding_config = {
            "padx": 2,
            "pady": 3,
        }

        event_label_height = 10

        event_button = customtkinter.CTkButton(hour_frame, text=f"{event.title}", height=event_label_height, anchor="w")
        event_button.pack(side="left", fill="both", expand=True, **padding_config)
        self.event_buttons.append(event_button)