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
