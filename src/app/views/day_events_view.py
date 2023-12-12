"""
DayEventsView class, which is the view of the day events state.
"""
import datetime
from typing import Mapping, List
import customtkinter
from src.app.views.view import View
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
        selected_day: A datetime.date object, the day that the user selected.
    """
    def __init__(self, root, day_events: Mapping[int, Mapping[int, List[Element]]], selected_day: datetime.date):
        super().__init__(root)
        self.selected_day = selected_day

        self.go_back_button = None
        self.event_name_entry = None
        self.event_description_textbox = None
        self.event_type_selector = None
        self.event_hour_selector = None
        self.event_minute_selector = None

        self.create_event_button = None
        self.update_event_button = None
        self.delete_event_button = None

        self.day_events = day_events

        self.event_management_frame = None
        self.today_events_frame = None

        self.hour_buttons = {}
        self.event_buttons = []

        self.currently_selected_event = None

        self.event_types = ["task", "reminder", "event"]
        self.currently_selected_hour = 0
        self.currently_selected_minute = 0
        self.event_management_title = None
        self.date_text = f"{self.selected_day.day}/{self.selected_day.month}/{self.selected_day.year}"

    def show(self):
        # confuring the grid:
        # +----------+-----------------+
        # |  event   |                 |
        # | managing |     Today's     |
        # |          |     events      |
        # |          |                 |
        # +----------+-----------------+

        self.root.grid_columnconfigure((0), weight=1) # event creation
        self.root.grid_columnconfigure((1), weight=2) # today's events

        self.show_event_managing()
        self.show_today_events()

    def show_event_managing(self):
        self.event_management_frame = customtkinter.CTkFrame(self.root)
        self.event_management_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.go_back_button = customtkinter.CTkButton(self.event_management_frame, text="Voltar")

        self.go_back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.event_name_entry = customtkinter.CTkEntry(self.event_management_frame)
        self.event_description_textbox = customtkinter.CTkTextbox(self.event_management_frame)
        self.event_type_selector = customtkinter.CTkOptionMenu(self.event_management_frame, values=self.event_types)
       
        self.show_time_picker()

        # event buttons, only loading
        self.create_event_button = customtkinter.CTkButton(self.event_management_frame, text="Criar evento")
        self.update_event_button = customtkinter.CTkButton(self.event_management_frame, text="Atualizar evento")
        self.delete_event_button = customtkinter.CTkButton(self.event_management_frame, text="Deletar evento")

        self.event_management_title = customtkinter.CTkLabel(self.event_management_frame, text=f"{self.date_text}: Selecione um horário para criar um evento, ou um evento para editá-lo.")
        self.event_management_title.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.show_event_creation_elements()


    def update_event_managing_elements(self):
        if self.currently_selected_event is None:
            self.hide_event_edditing_elements()
            self.show_event_creation_elements()
        else:
            self.hide_event_creation_elements()
            self.show_event_edditing_elements()
        self.event_hour_selector.set(f"{self.currently_selected_hour:02d}")
        self.event_minute_selector.set(f"{self.currently_selected_minute:02d}")

    def show_event_creation_elements(self):
        self.event_name_entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.event_description_textbox.grid(row=5, column=0, padx=10, pady=10, sticky="ew")
        self.event_type_selector.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.create_event_button.grid(row=6, column=0, padx=10, pady=10, sticky="ew")
        new_title = f"Criando um novo evento ({self.date_text})"
        self.event_management_title.configure(text=new_title)

    def hide_event_creation_elements(self):
        self.create_event_button.grid_forget()
        self.event_type_selector.grid_forget()
        # self.event_name_entry.grid_forget()
        # erase the event name
        self.event_name_entry.delete(0, "end")
        self.event_description_textbox.delete("0.0", "end")

    def show_event_edditing_elements(self):
        self.event_name_entry.insert(0, self.currently_selected_event.title)
        description = self.currently_selected_event.description 
        self.event_description_textbox.insert("0.0", description if description is not None else "")

        self.event_type_selector.set(self.currently_selected_event.element_type)
        self.event_name_entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.event_description_textbox.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        self.update_event_button.grid(row=6, column=0, padx=10, pady=10, sticky="ew")
        new_title = f"Editando {self.currently_selected_event.element_type}: \
            {self.currently_selected_event.title} ({self.date_text})"
        self.event_management_title.configure(text=new_title)

        self.delete_event_button.grid(row=7, column=0, padx=10, pady=20, sticky="e")

    def hide_event_edditing_elements(self):
        # self.event_name_entry.grid_forget()
        # self.event_type_selector.grid_forget()
        self.update_event_button.grid_forget()
        self.delete_event_button.grid_forget()
        # erase the event name
        self.event_name_entry.delete(0, "end")
        self.event_description_textbox.delete("0.0", "end")


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

    def show_hour_events(self, hour: int, hour_events: Mapping[int, List[Element]]):
        label_config = {
            "height": 20,
            "width": 40
        }

        padding_config = {
            "padx": 8,
            "pady": 3
        }

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
        self.event_buttons.append({
            "event": event,
            "button": event_button
        })

    def show_time_picker(self):
        # event time picker
        event_time_frame = customtkinter.CTkFrame(self.event_management_frame)
        event_time_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        time_picker_label = customtkinter.CTkLabel(event_time_frame, text="Horário do evento: (hh:mm)")
        time_picker_label.grid(row=0, column=0, padx=10, pady=2, sticky="ew")
        self.event_hour_selector = customtkinter.CTkOptionMenu(event_time_frame, values=[f"{hour:02d}" for hour in range(24)])
        self.event_hour_selector.grid(row=1, column=0, padx=4, pady=2, sticky="ew")
        self.event_minute_selector = customtkinter.CTkOptionMenu(event_time_frame, values=[f"{minute:02d}" for minute in range(0, 60, 10)])
        self.event_minute_selector.grid(row=1, column=1, padx=4, pady=2, sticky="ew")