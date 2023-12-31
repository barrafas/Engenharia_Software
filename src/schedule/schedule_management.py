""" Module for the ScheduleManagement class.

This module contains the ScheduleManagement class. This class is responsible
for managing the schedules in the database.

Classes:

    ScheduleManagement: Responsible for managing the schedules in the database
    
Exceptions:

    EmptyPermissionsError: Raised when the permissions list is empty
    DuplicatedIDError: Raised when the ID already exists
    NonExistentIDError: Raised when the ID does not exist

Functions:

    schedule_exists: Check if a schedule exists
    create_schedule: Create a new schedule
    get_schedule: Get a schedule by its ID
    update_schedule: Updates a schedule in the database
    delete_schedule: Deletes a schedule from the database and the schedules 
        dictionary
    add_element_to_schedule: Add an element to a schedule
    update: Called when the schedule is updated.
"""

from src.database.mongo_module import MongoModule,DuplicatedIDError,NonExistentIDError
from src.observer.observer import Observer, Subject, DatabaseNotProvidedError
from src.schedule.schedule_model import Schedule


class EmptyPermissionsError(Exception):
    """Raised when the permissions list is empty"""
    pass


class ScheduleManagement(Observer):
    """
    ScheduleManagement class
    Responsible for managing the schedules in the database

    Attributes:
        db: Database module
        schedules: Dictionary of schedules, where the key is the schedule ID
            and the value is the schedule instance
    """
    _instance = None

    @classmethod
    def get_instance(cls,
                    database_module: MongoModule = None,
                    schedules: dict = None) -> 'ScheduleManagement':
        """
        Get the instance of the ScheduleManagement class
        """
        if cls._instance is None:
            cls._instance = cls(database_module, schedules)
        return cls._instance

    def __init__(self,
                database_module: MongoModule,
                schedules: dict = None):
        """
        Constructor for the ScheduleManagement class

        Args:
            database_module: Database module

        """

        if not database_module:
            raise DatabaseNotProvidedError(
                "Database module not provided on object creation.")

        self.db_module = database_module
        self.schedules = schedules if schedules else {}

    def schedule_exists(self,
                        schedule_id: str) -> bool:
        """
        Check if a schedule exists

        Args:
            schedule_id: Schedule ID

        Returns:
            True if the schedule exists, False otherwise
        """

        # Get the schedules from the database that match the given ID
        schedule = self.db_module.select_data(
            'schedules', {'_id': schedule_id})
        # If the list is not empty, the schedule exists
        return bool(schedule)

    def create_schedule(self,
                        schedule_id: str,
                        title: str,
                        description: str,
                        permissions: dict,
                        elements: list) -> Schedule:
        """
        Create a new schedule

        Args:
            schedule_id: Schedule ID
            title: Title of the schedule
            description: Description of the schedule
            permissions: Dictionary of permissions, where the key is the user 
            elements: List of elements IDs that are displayed in the schedule

        Returns:
            The created schedule instance
        """
        from src.calendar_elements.element_management import ElementManagement
        from src.user.user_management import UserManagement

        # Possible errors:
        if self.schedule_exists(schedule_id):
            raise DuplicatedIDError(f"A schedule with ID {schedule_id} \
                                    already exists")
        if not isinstance(schedule_id, str):
            raise TypeError("Schedule ID must be a string")
        if not permissions:
            raise EmptyPermissionsError("Permissions cannot be empty")

        # Check if each element exists
        element_manager = ElementManagement.get_instance()
        for element_id in elements:
            if not element_manager.element_exists(element_id):
                raise NonExistentIDError(f"No element found \
                                         with ID {element_id}")

        # Check if each user exists
        user_manager = UserManagement.get_instance()
        for user_id in permissions.keys():
            if not user_manager.user_exists(user_id):
                raise NonExistentIDError(f"No user found with ID {user_id}")

        # Create the schedule instance and insert it into the database
        schedule = Schedule(schedule_id,
                            title,
                            description,
                            permissions,
                            elements)

        self.db_module.insert_data('schedules', {'_id': schedule_id,
                                                 'title': title,
                                                 'description': description,
                                                 'permissions': permissions,
                                                 'elements': elements})
        # Add the schedule to the dictionary
        self.schedules[schedule_id] = schedule

        # Update each element and add the schedule to its schedules attribute
        for element_id in elements:
            element = element_manager.get_element(element_id)
            element.schedules = element.schedules + [schedule_id]
        # Update each user and add the schedule to its schedules attribute
        for user_id in permissions.keys():
            user = user_manager.get_user(user_id)
            user.schedules = user.schedules + [schedule_id]
        schedule.attach(self)
        return schedule

    def get_schedule(self,
                     schedule_id: str) -> Schedule:
        """
        Get a schedule by its ID

        Args:
            schedule_id: Schedule ID

        Returns:
            The schedule instance
        """
        if schedule_id in self.schedules:
            return self.schedules[schedule_id]
        elif self.schedule_exists(schedule_id):
            schedule_data = self.db_module.select_data('schedules',
                                                       {'_id': schedule_id})[0]
            schedule = Schedule(schedule_id,
                                schedule_data['title'],
                                schedule_data['description'],
                                schedule_data['permissions'],
                                schedule_data['elements'])
            self.schedules[schedule_id] = schedule
            schedule.attach(self)
            return schedule
        else:
            raise NonExistentIDError(
                f"No schedule found with ID {schedule_id}")

    def update_schedule(self,
                        schedule_id: str) -> None:
        """
        Updates a schedule in the database

        Args:
            schedule_id: Schedule ID
        """
        if schedule_id not in self.schedules:
            raise NonExistentIDError(
                f"No schedule found with ID {schedule_id}")

        schedule = self.schedules[schedule_id]
        new_data = schedule.to_dict()
        self.db_module.update_data('schedules', {'_id': schedule_id}, new_data)

    def delete_schedule(self, schedule_id: str) -> None:
        """
        Deletes a schedule from the database and the schedules dictionary

        Args:
            schedule_id: Schedule ID
        """
        from src.calendar_elements.element_management import ElementManagement
        from src.user.user_management import UserManagement

        if not self.schedule_exists(schedule_id):
            raise NonExistentIDError(
                f"No schedule found with ID {schedule_id}")

        # Update each element
        schedule = self.get_schedule(schedule_id)
        element_manager = ElementManagement.get_instance()
        for element_id in schedule.elements:
            element = element_manager.get_element(element_id)
            element.schedules = [schedule for schedule in
                                 element.schedules if schedule != schedule_id]

        # Update each user
        user_ids = schedule.permissions.keys()
        user_manager = UserManagement.get_instance()
        for user_id in user_ids:
            user = user_manager.get_user(user_id)
            user.schedules = [schedule for schedule in
                              user.schedules if schedule != schedule_id]

        self.db_module.delete_data('schedules', {'_id': schedule_id})
        if schedule_id in self.schedules:
            remove = self.schedules.pop(schedule_id)
            del remove

    def add_element_to_schedule(self,
                                schedule_id: str,
                                element_id: str) -> None:
        """
        Add an element to a schedule

        Args:
            schedule_id: Schedule ID
            element_id: Element ID
        """
        from src.calendar_elements.element_management import ElementManagement

        element_manager = ElementManagement.get_instance()
        if not element_manager.element_exists(element_id):
            raise NonExistentIDError(f"No element found with ID {element_id}")

        if not self.schedule_exists(schedule_id):
            raise NonExistentIDError(
                f"No schedule found with ID {schedule_id}")

        schedule = self.get_schedule(schedule_id)
        if element_id not in schedule.elements:
            schedule.elements = schedule.elements + [element_id]
            element = element_manager.get_element(element_id)
            element.schedules = element.schedules + [schedule_id]
        else:
            raise DuplicatedIDError(f"Element with ID {element_id} already \
                                    exists in schedule {schedule_id}")

    def update(self,
               subject: Subject) -> None:
        """
        Called when the schedule is updated.

        Args:
            schedule: The schedule that was updated.
        """
        print(f"Schedule {subject.id} was updated.")
        self.update_schedule(subject.id)
