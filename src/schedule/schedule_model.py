from src.calendar_elements.element_interface import Element

class Schedule:
    """
        Class that represents a schedule:

        A schedule is a collection of elements that are displayed in the calendar.
        A schedule can be assigned to one or more users, and each user can have
        one or more schedules. 
        A schedule can be assigned to zero or more elements,
        and each element can be assigned to one or more schedules.
        Each user can have a different permission in a schedule.
    """
    def __init__(self, schedule_id: str, title: str, description: str, 
            permissions: [tuple] = None, elements: [Element] = None):
        """
            Schedule constructor.
            Arguments:
                schedule_id -- id of the schedule.
                title -- title of the schedule.
                description -- description of the schedule.
                permissions -- list of tuples (user_id, permission_type) 
                        that represent the permissions of the users in the schedule.
                elements -- list of elements that are displayed in the schedule.
        """
        self.id = schedule_id
        self.title = title
        self.description = description
        self.permissions = permissions if permissions else []
        self.elements = elements if elements else []

    @property
    def id(self):
        return self._id

    @property
    def permissions(self):
        return self._permissions

    @property
    def elements(self):
        return self._elements


    def get_elements(self) -> list:
        '''
            Returns a list of elements in the schedule.

            Returns:
                [Element] -- List of elements in the schedule.
        '''
        pass

    def get_users(self, permission_types = None) -> list:
        '''
            Returns a list of users that have the specified permission types.
            If no permission types are specified, returns all the users in the schedule.

            Arguments:
                permission_types -- list of permission types.

            Returns:
                [User] -- List of users that have the specified permission types.
        '''
        pass

    def set_title(self, title: str) -> None:
        '''
            Sets the title of the schedule.

            Arguments:
                title -- title of the schedule.
        '''
        pass

    def set_description(self, description: str) -> None:
        '''
            Sets the description of the schedule.

            Arguments:
                description -- description of the schedule.
        '''
        pass

    def to_dict(self) -> dict:
        '''
            Returns a dictionary representation of the schedule,
            which can be used to create a JSON object.

            Returns:
                dict -- Dictionary representation of the schedule.
        '''
        pass