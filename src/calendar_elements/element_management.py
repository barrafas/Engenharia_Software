from ..calendar_elements.element_interface import Element
from ..calendar_elements.element_factory import ElementFactory
from src.database.mongo_module import MongoModule
from src.database.database_module import DatabaseModule


class ElementManagement:
    """
        Class responsible for managing the elements in the database.

    Attributes:
        db: Database module.
        elements: Dictionary of elements, where the key is the element ID
            and the value is the element instance
    """

    _instance = None

    @classmethod
    def get_instance(cls, database_module: MongoModule, elements: dict = None):
        if cls._instance is None:
            cls._instance = cls(database_module, elements)
        return cls._instance

    def __init__(self, database_module: MongoModule, elements: dict = None):
        self.db_module = database_module
        self.elements = elements if elements is not None else {}

