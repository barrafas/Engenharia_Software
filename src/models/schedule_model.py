from datetime import datetime

class ScheduleModel:
    def __init__(self, schedule_id, title, description, events):
        self.schedule_id = schedule_id
        self.title = title
        self.description = description
        self.events = events  # Lista de objetos EventModel
