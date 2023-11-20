from datetime import datetime

from src.events.event_types import EventEvent, TaskEvent, ReminderEvent
from src.events.event_interface import Event

class EventFactory:
    @staticmethod
    def create_event(event_type, title, start=None, end=None, due_date=None):
        if event_type == "evento":
            return EventEvent(title, start, end)
        elif event_type == "tarefa":
            return TaskEvent(title)
        elif event_type == "lembrete":
            return ReminderEvent(title, due_date)
        else:
            raise ValueError("Tipo de evento desconhecido")
