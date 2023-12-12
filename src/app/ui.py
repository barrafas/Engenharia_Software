"""
Módulo responsável por gerenciar a interface gráfica do programa.
"""
import customtkinter
from src.app.views.splash_view import SplashView

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

class TkinterUI:
    """
    Classe responsável por gerenciar a interface gráfica do programa.
    """
    def __init__(self, app_context):
        self.app_context = app_context
        self.root = customtkinter.CTk()
        # Configuração de elementos da interface
        self.root.title("Sistema de Calendário")
        self.root.geometry(f"{800}x{600}")

        # Vincula o fechamento da janela e a tecla ESC a uma função
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.bind('<Escape>', self.close)

        # inicializa a view padrão
        self.view = SplashView(self.root)


    def show_day_events(self, day_events, day):
        # Lógica para exibir elementos relacionados ao login

        self.logout_button = customtkinter.CTkButton(self.root, text="Logout")
        self.logout_button.pack()

        self.go_back_button = customtkinter.CTkButton(self.root, text="Voltar")
        self.go_back_button.pack()

        self.create_event_button = customtkinter.CTkButton(self.root, text="Criar evento")
        self.create_event_button.pack()

        self.event_name_entry = customtkinter.CTkEntry(self.root)
        self.event_name_entry.pack()

        values = ["task", "reminder", "event"]
        self.event_type_selector = customtkinter.CTkOptionMenu(self.root, values=values)
        self.event_type_selector.pack()

        day_events_label = customtkinter.CTkLabel(self.root, text=f"Eventos do dia {day}")
        day_events_label.pack()

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
