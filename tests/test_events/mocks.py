from datetime import datetime, timedelta

class Schedule:

    def __init__(self, elements: list=None, users: list=None):
        self.elements = elements if elements else []
        self.users = users if users else []

    def get_elements(self, type: str=None):
        if type:
            return [element for element in self.elements if element.type == type]
        return self.elements
    
    def get_users(self, type: str=None):
        if type:
            return [user for user in self.users if user.type == type]
        return self.users
        
        

class ScheduleManagement:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        self.schedules = {
        'id1': Schedule(['elementid1', 'elementid2', 'elementid5']),
        'id2': Schedule(['elementid3', 'elementid4', 'elementid5']),
        'id3': Schedule(['elementid2', 'elementid6', 'elementid7'])
        }

    def get_schedule(self, id: str):
        return self.schedules[id]
    
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