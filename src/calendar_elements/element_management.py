"""
    Tests for the schedule manager class.
"""
from src.observer.observer import Observer, Subject, DatabaseNotProvidedError
from src.database.mongo_module import MongoModule, NonExistentIDError
from src.calendar_elements.element_factory import ElementFactory
from src.calendar_elements.element_interface import Element


class ElementDoesNotExistError(Exception):
    """
    Custom exception class for when a element does not exist.
    """


class ElementAlreadyExistsError(Exception):
    """
    Custom exception class for when a element already exists.
    """


class ElementManagement(Observer):
    """
        Class responsible for managing the elements in the database.

    Attributes:
        db: Database module.
        elements: Dictionary of elements, where the key is the element ID
            and the value is the element instance
    """

    _instance = None

    @classmethod
    def get_instance(cls, 
                     database_module: MongoModule = None,
                     elements: dict = None) -> 'ElementManagement':
        """
        Get the instance of the ElementManagement class.
        """
        if cls._instance is None:
            cls._instance = cls(database_module, elements)
        return cls._instance

    def __init__(self, database_module: MongoModule, elements: dict = None):
        """
        Constructor for the ElementManagement class.

        Args:
            database_module: Database module.
            elements: Dictionary of elements, where the key is the element ID
        """

        if not database_module:
            raise DatabaseNotProvidedError(
                "Database module not provided on object creation.")

        self.db_module = database_module
        self.elements = elements if elements is not None else {}

    def element_exists(self, element_id: str) -> bool:
        """
        Check if an element exists.

        Arguments:
            element_id: Element id.

        Returns:
            bool: True if the element exists, False otherwise.
        """
        element = self.db_module.select_data("elements", {"_id": element_id})
        return bool(element)

    def get_element(self, element_id: str) -> Element:
        """
        Get an element by its id.

        Arguments:
            element_id: Element id.

        Returns:
            Element: Element instance.
        """

        if element_id in self.elements:
            return self.elements[element_id]
        elif self.element_exists(element_id):
            element_data = self.db_module.select_data("elements",
                                                      {"_id": element_id})[0]
            element_data["element_id"] = element_data.pop("_id")
            element = ElementFactory.create_element(**element_data)
            self.elements[element_id] = element
            element.attach(self)
            return element
        else:
            raise ElementDoesNotExistError(
                f"Element with id {element_id} does not exist")

    def update_element(self, element_id: str) -> None:
        """
        Update an element.

        Arguments:
            element_id: element id.
            title: element title.
            kwargs: element arguments.
        """
        if not self.element_exists(element_id):
            raise ElementDoesNotExistError(
                f"Element with id {element_id} does not exist")

        element = self.elements[element_id]
        new_data = element.to_dict()
        self.db_module.update_data("elements", {"_id": element_id}, new_data)

    def delete_element(self, element_id: str) -> None:
        """
        Delete an element by its id.

        Arguments:
            element_id: Element id.
        """
        from src.schedule.schedule_management import ScheduleManagement

        if not self.element_exists(element_id):
            raise ElementDoesNotExistError(
                f"Element with id {element_id} does not exist")

        element = self.get_element(element_id)
        schedule_manager = ScheduleManagement.get_instance()
        for schedule in element.schedules:
            schedule_instance = schedule_manager.get_schedule(schedule)
            schedule_instance.elements = [element for element in
                                          schedule_instance.elements if element != element_id]

        self.db_module.delete_data('elements', {'_id': element_id})
        if element_id in self.elements:
            remove = self.elements.pop(element_id)
            del remove

    def create_element(self,
                       element_type: str,
                       element_id: str,
                       title: str,
                       schedules: list,
                       **kwargs) -> Element:
        """
        Create a new element.

        Arguments:
            element_type: Element type.
            element_id: Element id.
            title: Element title.
            kwargs: Element arguments.

        Returns:
            Element: Element instance.
        """
        if element_type not in ['event', 'task', 'reminder']:
            raise ValueError(f"Element is not a valid type ({element_type})")

        if not isinstance(element_id, str):
            raise TypeError("Element ID must be a string")

        if not isinstance(title, str):
            raise TypeError("Title must be a string")

        if not schedules:
            raise ValueError("Element must have at least one schedule")

        if not isinstance(schedules, list):
            raise TypeError("Schedules must be a list")

        for schedule in schedules:
            if not isinstance(schedule, str):
                raise TypeError("Schedule must be a string")

        if self.element_exists(element_id):
            raise ElementAlreadyExistsError(
                f"Element with id {element_id} already exists")

        # Check if each schedule exists
        from src.schedule.schedule_management import ScheduleManagement

        schedule_manager = ScheduleManagement.get_instance()
        for schedule_id in schedules:
            if not schedule_manager.schedule_exists(schedule_id):
                raise NonExistentIDError(
                    f"No schedule found with ID {schedule_id}")
        element = ElementFactory.create_element(element_type=element_type,
                                                element_id=element_id,
                                                title=title,
                                                schedules=schedules,
                                                **kwargs)
        element.attach(self)
        self.db_module.insert_data("elements", element.to_dict())
        self.elements[element_id] = element
        # Update each schedule
        for schedule in element.schedules:
            schedule_instance = schedule_manager.get_schedule(schedule)
            schedule_instance.elements = (
                schedule_instance.elements + [element_id])

        return element

    def update(self,
               element: Subject) -> None:
        """
        Called when the element is updated.

        Args:
            element: The element that was updated.
        """
        self.update_element(element.id)
