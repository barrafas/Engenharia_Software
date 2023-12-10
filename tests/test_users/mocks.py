from datetime import datetime, timedelta

class Schedule:
    def __init__(self, elements: list=None):
        self.elements = elements if elements else []

    def get_elements(self, type: str=None):
        if type:
            return [element for element in self.elements if element.type == type]
        return self.elements

class ScheduleManagement:
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = ScheduleManagement()
        return cls._instance


    def __init__(self):
        self.schedules = {
        'id1': Schedule(['elementid1', 'elementid2', 'elementid5']),
        'id2': Schedule(['elementid3', 'elementid4', 'elementid5']),
        'id3': Schedule(['elementid2', 'elementid6', 'elementid7'])
        }

    def get_schedule(self, id: str):
        return self.schedules[id]
    
class Element:
    def __init__(self, start_time: datetime, end_time: datetime, type: str):
        self.start_time = start_time
        self.end_time = end_time
        self.type = type

    def get_display_interval(self):
        return (self.start_time, self.end_time)
    
class ElementManagement:
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = ElementManagement()
        return cls._instance
    
    def __init__(self):
        self.elements = {
            'elementid1': Element(
                datetime.now(), datetime.now() + timedelta(hours=1), 'evento'),
            'elementid2': Element(
                datetime.now() + timedelta(hours=15), 
                datetime.now() + timedelta(hours=16), 'evento'),
            'elementid3': Element(
                datetime.now() + timedelta(hours=8), 
                datetime.now() + timedelta(hours=9), 'tarefa'),
            'elementid4': Element(
                datetime.now() + timedelta(hours=9), 
                datetime.now() + timedelta(hours=10), 'evento'),
            'elementid5': Element(
                datetime.now() + timedelta(hours=12), 
                datetime.now() + timedelta(hours=14), 'evento'),
            'elementid6': Element(
                datetime.now() + timedelta(hours=18), 
                datetime.now() + timedelta(hours=19), 'evento'),
            'elementid7': Element(
                datetime.now() + timedelta(hours=19), 
                datetime.now() + timedelta(hours=20), 'evento'),
        }

    def get_element(self, id: str):
        return self.elements[id]