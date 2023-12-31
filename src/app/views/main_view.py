"""
Main view is the view that shows the user's calendar.
"""
import customtkinter
from src.app.views.view import View
import datetime
import calendar

class MainView(View):
    """
    Main view is the view that shows the user's calendar.
    """
    def __init__(self, root, elements) -> None:
        super().__init__(root)

        self.logout_button = None
        self.go_back_button = None

        self.logged_user_name = ""

        self.elements = elements
        self.schedules = None
        self.selected_schedules_ids = None

        self.schedules_checkboxes = {}
        self.add_schedule_button = None

        self.sidebar = None
        self.navbar = None
        self.main_frame = None
        self.month_frame = None

        self.calendar_frame = None
        self.calendar_buttons = {}

        self.selected_date = datetime.date.today()

    def show(self):
        # confuring the grid:
        # +---------+-----------------+
        # | sidebar |     navbar      |
        # |         +-----------------+
        # |         |                 |
        # |         |      main       |
        # |         |                 |
        # |         |                 |
        # +---------+-----------------+

        self.root.grid_columnconfigure((0), weight=2) # sidebar
        self.root.grid_columnconfigure((1), weight=5) # navbar and main

        self.root.grid_rowconfigure((0), weight=1) # navbar
        self.root.grid_rowconfigure((1), weight=9) # main

        self.show_sidebar()
        self.show_navbar()
        self.show_main()

    def show_sidebar(self):
        self.sidebar = customtkinter.CTkFrame(self.root)
        self.sidebar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", rowspan=2)

        # sidebar elements
        self.show_sidebar_elements()

    def show_sidebar_elements(self):
        self.logout_button = customtkinter.CTkButton(self.sidebar, text="Logout")
        self.logout_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        schedules_frame = customtkinter.CTkFrame(self.sidebar)
        schedules_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        for schedule in self.schedules:
            schedule_checkbox = customtkinter.CTkCheckBox(schedules_frame, text=schedule.title)
            schedule_checkbox.pack(anchor="w", padx=10, pady=10, expand=True, fill="x")
            if schedule.id in self.selected_schedules_ids:
                schedule_checkbox.select()
            else:
                schedule_checkbox.deselect()
        
        self.add_schedule_button = customtkinter.CTkButton(self.sidebar, text="Adicionar agenda")
        self.add_schedule_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    def show_navbar(self):
        self.navbar = customtkinter.CTkFrame(self.root)
        self.navbar.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # navbar elements
        self.show_navbar_elements()

    def show_navbar_elements(self):
        self.logged_user_name_label = customtkinter.CTkLabel(self.navbar, text=f"Bem vindo {self.logged_user_name}!")
        self.logged_user_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="we")

        self.go_back_button = customtkinter.CTkButton(self.navbar, text="Voltar")
        self.go_back_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

    def show_main(self):
        self.main_frame = customtkinter.CTkFrame(self.root)
        self.main_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")


        # main elements
        self.show_main_elements()

    def show_main_elements(self):
        user_events_label = customtkinter.CTkLabel(self.main_frame, text="Eventos do usuário")
        user_events_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.month_frame = customtkinter.CTkFrame(self.main_frame)
        self.month_frame.grid(row=1, column=0, padx=1, pady=1, sticky="nsew")

        self.show_calendar()
        self.show_next_month()
        self.show_previous_month()
        
        self.export_data_button = customtkinter.CTkButton(self.sidebar, text="Exportar dados")
        self.export_data_button.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    def show_calendar(self):
        self.calendar_frame = customtkinter.CTkFrame(self.main_frame)
        self.calendar_frame.grid(row=2, column=0, padx=1, pady=1, sticky="nsew")

        # configuring the grid to be 7x8
        for column in range(7):
            self.calendar_frame.grid_columnconfigure((column), weight=1)
        for row in range(8):
            self.calendar_frame.grid_rowconfigure((row), weight=1)

        # calendar elements
        self.show_calendar_elements()

    def show_calendar_elements(self):
        year = self.selected_date.year
        month = self.selected_date.month

        title = f"{calendar.month_name[month]} {year}"

        calendar_title = customtkinter.CTkLabel(self.calendar_frame, text=title)
        calendar_title.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=7)

        cal = calendar.TextCalendar(calendar.SUNDAY)
        calendar_day_size = {
            "width": 50,
            "height": 40
        }

        for w, week in enumerate(cal.monthdayscalendar(year, month), 2):
            for d, day in enumerate(week):
                if day != 0:
                    day_button = customtkinter.CTkButton(self.calendar_frame, text=day, width=calendar_day_size["width"], height=calendar_day_size["height"])
                    day_button.grid(row=w, column=d, padx=1, pady=1, sticky="nsew")
                    self.calendar_buttons[(year, month, day)] = day_button
                else:
                    day_button = customtkinter.CTkButton(self.calendar_frame, text=" ", width=calendar_day_size["width"], height=calendar_day_size["height"])
                    day_button.grid(row=w, column=d, padx=1, pady=1, sticky="nsew")

    def show_next_month(self):
        self.next_month_button = customtkinter.CTkButton(self.month_frame, text=">", width=50, height=2)
        self.next_month_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    def show_previous_month(self):
        self.prev_month_button = customtkinter.CTkButton(self.month_frame, text="<", width=50, height=2)
        self.prev_month_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
