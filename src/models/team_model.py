class TeamMember:
    def __init__(self, user_id, role):
        self.user_id = user_id
        self.role = role

class TeamModel:
    def __init__(self, team_id, name, members):
        self.team_id = team_id
        self.name = name
        self.members = members  # Lista de objetos TeamMember
