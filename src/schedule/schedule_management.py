from src.schedule.schedule_model import Schedule

class ScheduleManagement:
    """
    ScheduleManagement class
    Responsible for managing the schedules in the database

    Attributes:
        db: Database module
        schedules: Dictionary of schedules, where the key is the schedule ID
            and the value is the schedule instance
    """

    def __init__(self, database_module: DatabaseModule, schedules: dict = None):
        """
        Constructor for the ScheduleManagement class

        Args:
            database_module: Database module

        """
        self.db = database_module

    def create_schedule(self, title: str, description: str, 
            permissions: [tuple], schedule_id: str = None) -> Schedule:
        """
        Create a new schedule

        Args:
            title: Title of the schedule
            description: Description of the schedule
            permissions: List of tuples (user_id, permission_type)
            schedule_id: Schedule ID

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

    def schedule_exists(self, schedule_id: str) -> bool:
        """
        Check if a schedule exists

        Args:
            schedule_id: Schedule ID

        Returns:
            True if the schedule exists, False otherwise
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