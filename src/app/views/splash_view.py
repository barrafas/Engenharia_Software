"""
Splash view is the view that shows the login and sign up buttons.
"""
import customtkinter
from src.app.views.view import View


class SplashView(View):
    """
    Splash view is the view that shows the login and sign up buttons.
    """
    def __init__(self, root) -> None:
        super().__init__(root)

        self.login_button = None
        self.sign_up_button = None

        self.database_url_entry = None
        self.database_port_entry = None
        self.database_user_entry = None
        self.database_password_entry = None

    def show(self):
        login_label = customtkinter.CTkLabel(self.root, text="Já possui uma conta?")
        login_label.pack()
        login_button = customtkinter.CTkButton(self.root, text="Faça login")
        login_button.pack()

        sign_up_label = customtkinter.CTkLabel(self.root, text="Não possui uma conta?")
        sign_up_label.pack()
        sign_up_button = customtkinter.CTkButton(self.root, text="Cadastre-se")
        sign_up_button.pack()

        self.login_button = login_button
        self.sign_up_button = sign_up_button

        self.show_database_config()

    def show_database_config(self):
        database_frame = customtkinter.CTkFrame(self.root)
        database_frame.pack(pady=50)

        database_url_label = customtkinter.CTkLabel(database_frame, text="Database URL:")
        database_url_label.grid(row=0, column=0)
        database_url_entry = customtkinter.CTkEntry(database_frame)
        database_url_entry.grid(row=0, column=1)

        database_port_label = customtkinter.CTkLabel(database_frame, text="Database Port:")
        database_port_label.grid(row=1, column=0)
        database_port_entry = customtkinter.CTkEntry(database_frame)
        database_port_entry.grid(row=1, column=1)

        database_user_label = customtkinter.CTkLabel(database_frame, text="DB User:")
        database_user_label.grid(row=2, column=0)
        database_user_entry = customtkinter.CTkEntry(database_frame)
        database_user_entry.grid(row=2, column=1)

        database_password_label = customtkinter.CTkLabel(database_frame, text="DB Password:")
        database_password_label.grid(row=3, column=0)
        database_password_entry = customtkinter.CTkEntry(database_frame, show="*")
        database_password_entry.grid(row=3, column=1)

        database_url_entry.insert(0, self.database_url_entry)
        database_port_entry.insert(0, self.database_port_entry)
        database_user_entry.insert(0, self.database_user_entry)
        database_password_entry.insert(0, self.database_password_entry)

        self.database_url_entry = database_url_entry
        self.database_port_entry = database_port_entry
        self.database_user_entry = database_user_entry
        self.database_password_entry = database_password_entry
