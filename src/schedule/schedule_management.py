from src.schedule.schedule_model import Schedule
from src.database.mongo_module import MongoModule
from src.user.user_model import User
from src.user.user_management import UserManagement
from tests.test_schedule.mocks import Element, ElementManagement


class EmptyPermissionsError(Exception):
    """Raised when the permissions list is empty"""
    pass

class DuplicatedIDError(Exception):
    """Raised when the ID already exists"""
    pass

class NonExistentIDError(Exception):
    """Raised when the ID does not exist"""
    pass

class ScheduleManagement:
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
    def get_instance(cls, database_module: MongoModule, schedules: dict = None):
        if cls._instance is None:
            cls._instance = cls(database_module, schedules)
        return cls._instance

    def __init__(self, database_module: MongoModule, schedules: dict = None):
        """
        Constructor for the ScheduleManagement class

        Args:
            database_module: Database module

        """
        self.db_module = database_module
        self.schedules = schedules if schedules else {}

    def schedule_exists(self, schedule_id: str) -> bool:
        """
        Check if a schedule exists

        Args:
            schedule_id: Schedule ID

        Returns:
            True if the schedule exists, False otherwise
        """

        # Get the schedules from the database that match the given ID
        schedule = self.db_module.select_data('schedules', {'_id': schedule_id})
        # If the list is not empty, the schedule exists
        return bool(schedule)
        

    def create_schedule(self, schedule_id: str, title: str, description: str, 
            permissions: dict, elements: list) -> Schedule:
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
        # Possible errors:
        if self.schedule_exists(schedule_id):
            raise DuplicatedIDError(f"A schedule with ID {schedule_id} already exists")
        if not isinstance(schedule_id, str):
            raise TypeError("Schedule ID must be a string")
        if not permissions:
            raise EmptyPermissionsError("Permissions cannot be empty")
        # Create the schedule instance and insert it into the database
        schedule = Schedule(schedule_id, title, description, permissions, elements)
        self.db_module.insert_data('schedules', {'_id': schedule_id, 
                                                 'title': title, 
                                                 'description': description, 
                                                 'permissions': permissions,
                                                    'elements': elements})
        # Add the schedule to the dictionary
        self.schedules[schedule_id] = schedule
        return schedule

    def get_schedule(self, schedule_id: str) -> Schedule:
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
            schedule_data = self.db_module.select_data('schedules', {'_id': schedule_id})
            schedule = Schedule(schedule_id, 
                                schedule_data['title'], 
                                schedule_data['description'], 
                                schedule_data['permissions'], 
                                schedule_data['elements'])
            self.schedules[schedule_id] = schedule
            return schedule
        else:
            raise NonExistentIDError(f"No schedule found with ID {schedule_id}")

    def update_schedule(self, schedule_id: str) -> None:
        """
        Updates a schedule in the database

        Args:
            schedule_id: Schedule ID
        """
        if schedule_id not in self.schedules:
            raise NonExistentIDError(f"No schedule found with ID {schedule_id}")

        schedule = self.schedules[schedule_id]
        new_data = schedule.to_dict()
        self.db_module.update_data('schedules', {'_id': schedule_id}, new_data)

    def delete_schedule(self, schedule_id: str) -> None:
        """
        Deletes a schedule from the database and the schedules dictionary

        Args:
            schedule_id: Schedule ID
        """
        if not self.schedule_exists(schedule_id):
            raise NonExistentIDError(f"No schedule found with ID {schedule_id}")

        self.db_module.delete_data('schedules', {'_id': schedule_id})
        if schedule_id in self.schedules:
            del self.schedules[schedule_id]


    def add_element_to_schedule(self, schedule_id: str, element_id: str) -> None:
        """
        Add an element to a schedule

        Args:
            schedule_id: Schedule ID
            element_id: Element ID
        """
        schedule = self.schedules[schedule_id]
        if element_id not in schedule.elements:
            schedule.elements = schedule.elements + [element_id]