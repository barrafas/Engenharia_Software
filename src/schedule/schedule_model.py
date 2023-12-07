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
            permissions: [tuple] = None, elements: [str] = None):
        """
            Schedule constructor.
            Arguments:
                schedule_id -- id of the schedule.
                title -- title of the schedule.
                description -- description of the schedule.
                permissions -- list of tuples (user_id, permission_type) 
                        that represent the permissions of the users in the schedule.
                elements -- list of elements ids that are displayed in the schedule.
        """
        self.__id = schedule_id
        self.set_title(title)
        self.set_description(description)
        self.__permissions = permissions if permissions else []
        self.__elements = elements if elements else []

    @property
    def id(self):
        return self.__id

    @property
    def permissions(self):
        return self.__permissions

    @property
    def elements(self):
        return self.__elements


    def get_elements(self) -> list:
        '''
            Returns a list of elements IDs for elements that are displayed in the schedule.

            Returns:
                [str] -- List of elements IDs in the schedule.
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
        if title is None:
            raise ValueError("Title cannot be None")
        if not isinstance(title, str):
            raise TypeError("Title must be a string")
        if len(title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if len(title) > 50:
            raise ValueError("Title must have at most 50 characters")
        self.title = title

    def set_description(self, description: str) -> None:
        '''
            Sets the description of the schedule.

            Arguments:
                description -- description of the schedule.
        '''
        if description is not None:
            if type(description) != str:
                raise TypeError("Description must be a string")
            elif len(description) > 500:
                raise ValueError("Description cannot have more than 500 characters")
        self.description = description

    def to_dict(self) -> dict:
        '''
            Returns a dictionary representation of the schedule,
            which can be used to create a JSON object.

            Returns:
                dict -- Dictionary representation of the schedule.
        '''
        pass