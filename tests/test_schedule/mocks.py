from datetime import datetime, timedelta

    
class Element:
    def __init__(self, start_time: datetime, end_time: datetime, element_type: str):
        self.start_time = start_time
        self.end_time = end_time
        self.type = element_type
    
class ElementManagement:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.elements = {
            'elementid1': Element(
                datetime.now(), datetime.now() + timedelta(hours=1), 'evento'),
            'elementid2': Element(
                datetime.now() + timedelta(hours=15), 
                datetime.now() + timedelta(hours=16), 'tarefa'),
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

    def get_element(self, element_id: str) -> Element:
        return self.elements[element_id]

class User:
    def __init__(self, user_id: str):
        self.__id = user_id

    @property
    def id(self):
        return self.__id

class UserManagement:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.users = {
            'userid1': User('userid1'),
            'userid2': User('userid2'),
            'userid3': User('userid3'),
            'userid4': User('userid4'),
            'userid5': User('userid5'),
            'userid6': User('userid6'),
            'userid7': User('userid7'),
            'userid8': User('userid8'),
            'userid9': User('userid9'),
            'userid10': User('userid10'),
        }

    def get_user(self, user_id: str) -> User:
        return self.users[user_id]