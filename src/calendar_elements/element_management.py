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
    def get_instance(cls, database_module: DatabaseModule = None, elements: dict = None):
        if cls._instance is None:
            cls._instance = cls(database_module, elements)
        return cls._instance

    def __init__(self, database_module: DatabaseModule, elements: dict = None):
        self.db_module = database_module
        self.elements = elements if elements is not None else {}

