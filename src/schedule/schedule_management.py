from src.schedule.schedule_model import Schedule
from src.database.mongo_module import MongoModule

class EmptyPermissionsException(Exception):
    """Raised when the permissions list is empty"""
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

        pass

    def get_schedule(self, schedule_id: str) -> Schedule:
        """
        Get a schedule by its ID

        Args:
            schedule_id: Schedule ID

        Returns:
            The schedule instance
        """

        pass

    def update_schedule(self, schedule_id) -> None:
        """
        Updates a schedule in the database

        Args:
            schedule_id: Schedule ID

        """

        pass

    def delete_schedule(self, schedule_id: str) -> None:
        """
        Deletes a schedule from the database

        Args:
            schedule_id: Schedule ID

        """

        pass


    def add_element_to_schedule(self, schedule_id: str, element_id: str) -> None:
        """
        Add an element to a schedule

        Args:
            schedule_id: Schedule ID
            element_id: Element ID
        """

        pass