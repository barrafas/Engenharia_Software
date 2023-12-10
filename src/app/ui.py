"""
Módulo responsável por gerenciar a interface gráfica do programa.
"""
import customtkinter
from .ui_main import MainUI

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class TkinterUI:
    """
    Classe responsável por gerenciar a interface gráfica do programa.
    """
    def __init__(self, app_context):
        self.app_context = app_context
        self.root = customtkinter.CTk()
        # Configuração de elementos da interface
        self.root.title("Sistema de Calendário")
        self.root.geometry(f"{450}x{300}")

        # Vincula o fechamento da janela e a tecla ESC a uma função
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.bind('<Escape>', self.close)


    def show_login_elements(self):
        # Lógica para exibir elementos relacionados ao login
        username_label = customtkinter.CTkLabel(self.root, text="Usuário")
        username_label.pack()
        username_entry = customtkinter.CTkEntry(self.root)
        username_entry.pack()

        password_label = customtkinter.CTkLabel(self.root, text="Senha")
        password_label.pack()
        password_entry = customtkinter.CTkEntry(self.root, show="*")
        password_entry.pack()

        login_button = customtkinter.CTkButton(self.root, text="Login")
        login_button.pack()

        go_back_button = customtkinter.CTkButton(self.root, text="Voltar")
        go_back_button.pack()

        self.username_entry = username_entry
        self.password_entry = password_entry
        self.login_button = login_button
        self.go_back_button = go_back_button

    def show_sign_in_up_elements(self):
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

    def show_main_elements(self):

        # logout_button = customtkinter.CTkButton(self.root, text="Logout")
        # logout_button.pack()

        # go_back_button = customtkinter.CTkButton(self.root, text="Voltar")
        # go_back_button.pack()

        # user_events_label = customtkinter.CTkLabel(self.root, text="Eventos do usuário")
        # user_events_label.pack()
        # user_events = customtkinter.CTkLabel(self.root, text=">> User events: loading... ")
        # user_events.pack()

        # self.logout_button = logout_button
        # self.go_back_button = go_back_button
        # self.user_events = user_events

        main_ui = MainUI(self.root)

        self.logout_button = main_ui.logout_button
        self.go_back_button = main_ui.go_back_button
        self.user_events = main_ui.user_events

    def show_sign_up_elements(self):
        # Lógica para exibir elementos relacionados ao login
        username_label = customtkinter.CTkLabel(self.root, text="Usuário")
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

        self.username_entry = username_entry
        self.email_entry = email_entry
        self.password_entry = password_entry
        self.sign_up_button = sign_up_button
        self.go_back_button = go_back_button

    def clear_elements(self):
        # Lógica para limpar elementos da interface
        for child in self.root.winfo_children():
            child.destroy()
        
    def run(self):
        self.root.mainloop()

    def close(self, event=None):
        # Função para executar quando a janela é fechada
        print("A janela foi fechada")
        self.root.destroy()
        self.app_context.close()
        self.root.quit()
        
