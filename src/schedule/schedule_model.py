""" Module that contains the Schedule class.
The Schedule class represents a schedule in the calendar.

Classes:

    Schedule -- Class that represents a schedule in the calendar.
"""

from src.observer.observer import Observer, Subject

class Schedule(Subject):
    """
        Class that represents a schedule:

        A schedule is a collection of elements that are displayed in the 
        calendar. A schedule can be assigned to one or more users, and each 
        user can have one or more schedules. 
        A schedule can be assigned to zero or more elements,
        and each element can be assigned to one or more schedules.
        Each user can have a different permission in a schedule.
    """

    def __init__(self,
                 schedule_id: str,
                 title: str,
                 description: str,
                 permissions: dict,
                 elements: [str] = None):
        """
            Schedule constructor.
            Arguments:
                schedule_id -- id of the schedule.
                title -- title of the schedule.
                description -- description of the schedule.
                permissions -- dict where the key is the user id and the value
                                 is the permission type.
                elements -- list of elements ids that are displayed in the 
                            schedule.
        """
        self.__observers = []
        self.__id = schedule_id
        self.set_title(title)
        self.set_description(description)
        self.__permissions = permissions
        self.__elements = elements if elements else []

    @property
    def id(self):
        """ method that returns the id of the schedule """
        return self.__id

    @property
    def permissions(self):
        """ method that returns the permissions of the schedule """
        return self.__permissions

    @property
    def elements(self):
        """ method that returns the elements of the schedule """
        return self.__elements

    @property
    def observers(self):
        """ method that returns the observers of the schedule """
        return self.__observers

    @permissions.setter
    def permissions(self, value):
        if isinstance(value, dict) \
                and all(isinstance(i, str) for i in value.keys()) \
                and all(isinstance(i, str) for i in value.values()):
            self.__permissions = value
            self.notify()
        else:
            raise TypeError("Permissions must be a dictionary of strings")

    @elements.setter
    def elements(self, value):
        if isinstance(value, list) and all(isinstance(i, str) for i in value):
            self.__elements = value
            self.notify()
        else:
            raise TypeError("Elements must be a list of strings")

    def get_elements(self, types=[]) -> list:
        """
            Returns a list of elements IDs for elements that are displayed in 
            the schedule.

            Arguments:
                types -- list of element types.

            Returns:
                [Element] -- List of element instances in the schedule that 
                have the specified types.
        """
        from src.calendar_elements.element_management import ElementManagement

        element_management = ElementManagement.get_instance()
        elements = []
        for element_id in self.__elements:
            element = element_management.get_element(element_id)
            if not types or element.type in types:
                elements.append(element)
        return elements

    def get_users(self, permission_types=[]) -> list:
        """
            Returns a list of users that have the specified permission types.
            If no permission types are specified, returns all the users in the 
            schedule.

            Arguments:
                permission_types -- list of permission types.

            Returns:
                [User] -- List of users that have the specified permission types
        """
        from src.user.user_management import UserManagement

        user_management = UserManagement.get_instance()
        users = []
        for user_id, permission_type in self.__permissions.items():
            if not permission_types or permission_type in permission_types:
                user = user_management.get_user(user_id)
                users.append(user)
        return users

    def set_title(self, title: str) -> None:
        """
            Sets the title of the schedule.

            Arguments:
                title -- title of the schedule.
        """
        if title is None:
            raise ValueError("Title cannot be None")
        if not isinstance(title, str):
            raise TypeError(f"Title must be a string, {type(title)} given]")
        if len(title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if len(title) > 50:
            raise ValueError("Title must have at most 50 characters")
        self.title = title
        self.notify()

    def set_description(self, description: str) -> None:
        """
            Sets the description of the schedule.

            Arguments:
                description -- description of the schedule.
        """
        if description is not None:
            if type(description) != str:
                raise TypeError("Description must be a string")
            elif len(description) > 500:
                raise ValueError("Description cannot have more than  \
                                 500 characters")
        self.description = description
        self.notify()

    def to_dict(self) -> dict:
        """
            Returns a dictionary representation of the schedule,
            which can be used to create a JSON object.

            Returns:
                dict -- Dictionary representation of the schedule.
        """
        return {
            "_id": self.__id,
            "title": self.title,
            "description": self.description,
            "permissions": self.__permissions,
            "elements": self.__elements
        }

    def attach(self, observer: Observer) -> None:
        """
            Attach an observer to the subject.

            Arguments:
                observer -- the observer to attach.
        """
        self.__observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """
            Detach an observer from the subject.

            Arguments:
                observer -- the observer to detach.
        """
        self.__observers.remove(observer)

    def notify(self) -> None:
        """
            Notify all the observers that the subject has changed.
        """
        for observer in self.__observers:
            observer.update(self)
