"""
Login view is the view where the user is supposed to put his credentials.
"""
import customtkinter
from src.app.views.view import View

class LoginView(View):
    """
    Login view is the view where the user is supposed to put his credentials.
    """
    def __init__(self, root) -> None:
        super().__init__(root)

        self.user_id_entry = None
        self.password_entry = None
        self.login_button = None
        self.go_back_button = None

    def show(self):
        user_id_label = customtkinter.CTkLabel(self.root, text="Username")
        user_id_label.pack()
        user_id_entry = customtkinter.CTkEntry(self.root)
        user_id_entry.pack()

        password_label = customtkinter.CTkLabel(self.root, text="Senha")
        password_label.pack()
        password_entry = customtkinter.CTkEntry(self.root, show="*")
        password_entry.pack()

        login_button = customtkinter.CTkButton(self.root, text="Login")
        login_button.pack()

        go_back_button = customtkinter.CTkButton(self.root, text="Voltar")
        go_back_button.pack()

        user_id_entry.focus()

        self.user_id_entry = user_id_entry
        self.password_entry = password_entry
        self.login_button = login_button
        self.go_back_button = go_back_button
