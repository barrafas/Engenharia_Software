from src.events.event_interface import Event

class EventEvent(Event):
    def __init__(self, id, title, start, end):
        self.id = id
        self.title = title
        self.start = start
        self.end = end

    def display_info(self):
        print(f"Evento: {self.title}, Início: {self.start}, Fim: {self.end}")

    def get_id(self):
        return self.id

class TaskEvent(Event):
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def display_info(self):
        print(f"Tarefa: {self.title}")

    def get_id(self):
        return self.id

class ReminderEvent(Event):
    def __init__(self, id, title, due_date):
        self.id = id
        self.title = title
        self.due_date = due_date

    def display_info(self):
        print(f"Lembrete: {self.title}, Data de Vencimento: {self.due_date}")

    def get_id(self):
        return self.id