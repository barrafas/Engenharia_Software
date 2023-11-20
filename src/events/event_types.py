from src.events.event_interface import Event

class EventEvent(Event):
    def __init__(self, title, start, end):
        self.title = title
        self.start = start
        self.end = end

    def display_info(self):
        print(f"Evento: {self.title}, Início: {self.start}, Fim: {self.end}")

class TaskEvent(Event):
    def __init__(self, title):
        self.title = title

    def display_info(self):
        print(f"Tarefa: {self.title}")

class ReminderEvent(Event):
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date

    def display_info(self):
        print(f"Lembrete: {self.title}, Data de Vencimento: {self.due_date}")
