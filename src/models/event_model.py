class EventModel:
    def __init__(self, event_id, title, start, end):
        self.event_id = event_id
        self.title = title
        self.start = start
        self.end = end

    def display_info(self):
        print(f"Evento: {self.title}, Início: {self.start}, Fim: {self.end}")

class TaskModel(EventModel):
    def __init__(self, event_id, title):
        super().__init__(event_id, title, None, None)

    # Adicione métodos ou atributos específicos para tarefas, se necessário

class ReminderModel(EventModel):
    def __init__(self, event_id, title, due_date):
        super().__init__(event_id, title, due_date, due_date)

    # Adicione métodos ou atributos específicos para lembretes, se necessário
