"""
Sign up view, where the user is supposed to put his credentials.
"""
import customtkinter
from src.app.views.view import View

class SignUpView(View):
    """
    Sign up view, where the user is supposed to put his credentials.
    """
    def __init__(self, root) -> None:
        super().__init__(root)

        self.user_id_entry = None
        self.username_entry = None
        self.email_entry = None
        self.password_entry = None
        self.sign_up_button = None
        self.go_back_button = None

    def show(self):
        user_id_label = customtkinter.CTkLabel(self.root, text="Username (Seu usuário para login)")
        user_id_label.pack()
        user_id_entry = customtkinter.CTkEntry(self.root)
        user_id_entry.pack()

        username_label = customtkinter.CTkLabel(self.root, text="Nome (seu nome de exibição)")
        username_label.pack()
        username_entry = customtkinter.CTkEntry(self.root)
        username_entry.pack()

        email_label = customtkinter.CTkLabel(self.root, text="Email")
        email_label.pack()
        email_entry = customtkinter.CTkEntry(self.root)
        email_entry.pack()

        password_label = customtkinter.CTkLabel(self.root, text="Senha")
        password_label.pack()
        password_entry = customtkinter.CTkEntry(self.root, show="*")
        password_entry.pack()

        sign_up_button = customtkinter.CTkButton(self.root, text="Cadastrar")
        sign_up_button.pack()

        go_back_button = customtkinter.CTkButton(self.root, text="Voltar")
        go_back_button.pack()

        user_id_entry.focus()

        self.user_id_entry = user_id_entry
        self.username_entry = username_entry
        self.email_entry = email_entry
        self.password_entry = password_entry
        self.sign_up_button = sign_up_button
        self.go_back_button = go_back_button
