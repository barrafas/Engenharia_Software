import customtkinter
import datetime
import calendar

class MainUI:
    def __init__(self, root):
        self.root = root
        self.logout_button = None
        self.go_back_button = None
        self.user_events = None

        self.sidebar = None
        self.navbar = None
        self.main_frame = None

        self.calendar = None
        self.calendar_title = None

        self.selected_date = datetime.date.today()

        # render the UI
        self.show_elements()

    def show_elements(self):
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
    
    def show_navbar(self):
        self.navbar = customtkinter.CTkFrame(self.root)
        self.navbar.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # navbar elements
        self.show_navbar_elements()

    def show_navbar_elements(self):
        self.go_back_button = customtkinter.CTkButton(self.navbar, text="Voltar")
        self.go_back_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    def show_main(self):
        self.main_frame = customtkinter.CTkFrame(self.root)
        self.main_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # main elements
        self.show_main_elements()

    def show_main_elements(self):
        self.user_events_label = customtkinter.CTkLabel(self.main_frame, text="Eventos do usuário")
        self.user_events_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # self.user_events = customtkinter.CTkLabel(self.main_frame, text=">> User events: loading... ")
        # self.user_events.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.show_calendar()

    def show_calendar(self):
        self.calendar = customtkinter.CTkFrame(self.main_frame)
        self.calendar.grid(row=2, column=0, padx=1, pady=1, sticky="nsew")

        # configuring the grid to be 7x8
        for column in range(7):
            self.calendar.grid_columnconfigure((column), weight=1)
        for row in range(8):
            self.calendar.grid_rowconfigure((row), weight=1)

        # calendar elements
        self.show_calendar_elements()

    def show_calendar_elements(self):
        year = self.selected_date.year
        month = self.selected_date.month

        month_calendar = calendar.month(year, month)
        title = f"{calendar.month_name[month]} {year}"

        self.calendar_title = customtkinter.CTkLabel(self.calendar, text=title)
        self.calendar_title.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=7)
                
        cal = calendar.TextCalendar(calendar.SUNDAY)
        calendar_day_size = {
            "width": 50,
            "height": 40
        }
        for w, week in enumerate(cal.monthdayscalendar(year, month), 2):
            for d, day in enumerate(week):
                if day != 0:
                    day_button = customtkinter.CTkButton(self.calendar, text=day, width=calendar_day_size["width"], height=calendar_day_size["height"])
                    day_button.grid(row=w, column=d, padx=1, pady=1, sticky="nsew")
                else:
                    day_button = customtkinter.CTkButton(self.calendar, text=" ", width=calendar_day_size["width"], height=calendar_day_size["height"])
                    day_button.grid(row=w, column=d, padx=1, pady=1, sticky="nsew")
        