class UserModel:
    def __init__(self, user_id, username, email, events=None, hashed_password=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.events = events if events else []
        self.hashed_password = hashed_password

    def __str__(self):
        return f"User({self.user_id}, {self.username}, {self.email}, {self.events})"

    def to_json(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "password": self.hashed_password,
            "events": self.events
        }
    
    @classmethod
    def from_json(cls, user_data):
        return cls(
            user_id         = user_data['user_id'],
            username        = user_data['username'],
            email           = user_data['email'],
            events          = user_data['events'],
            hashed_password = user_data['password']
        )
    
    def get_hashed_password(self):
        return self.hashed_password
    
    def __repr__(self):
        return " <User>:"+str(self.to_json())