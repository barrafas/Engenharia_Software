class User:
    def __init__(self, id: str, username: str, email: str, schedules: list=None, 
                 hashed_password: str=None, user_preferences: dict=None):
        self.id = id
        self.username = username
        self.email = email
        self.schedules = schedules if schedules else []
        self.hashed_password = hashed_password
        self.user_preferences = user_preferences if user_preferences else {}

    def __str__(self):
        return f"User({self.user_id}, {self.username}, {self.email}, {self.events})"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "schedules": self.schedules,
            "password": self.hashed_password,
            "user_preferences": self.user_preferences
        }
    
    def get_schedules(self):
        return self.schedules
    
    def get_elements(self, schedules: list=None):
        '''
        returns a list of ids of elements of all schedules (or only specific ones) 
        that the user is a part of  
        '''
        if not schedules:
            schedules = self.schedules
        # necessário ter ScheduleManagement e ElementManagement para implementar

    def get_hashed_password(self):
        return self.hashed_password
    
    def set_username(self, username: str):
        self.username = username
    
    def set_email(self, email: str):
        self.email = email

    def check_disponibility(self, time: tuple):
        element_ids = self.get_elements()
        # fazer query no banco de dados comparando o horário com os horários
        # dos elementos da seguinte forma:
        # verificar se em algum dos elementos, a condição
        #  time[0] > element.end_time ou time[1] < element.start_time é falsa.


    def __repr__(self):
        return " <User>:"+str(self.to_dict())