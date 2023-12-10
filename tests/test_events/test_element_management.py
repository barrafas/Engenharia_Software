import unittest
from unittest.mock import Mock, MagicMock, patch
from src.calendar_elements.element_management import ElementManagement, ElementAlreadyExistsError, ElementDoesNotExistError
from src.calendar_elements.element_factory import ElementFactory
from src.database.mongo_module import MongoModule
from src.calendar_elements.element_interface import Element

class TestElementManagement(unittest.TestCase):
    """ Tests for ElementManagement class """
    def setUp(self):
        # Reset singleton instance and create a mock database module
        ElementManagement._instance = None
        self.db_module = Mock(spec=MongoModule)
        self.element_management = ElementManagement.get_instance(self.db_module)

    def test_get_instance_creates_instance(self):
        """ Check that get_instance creates an instance of ElementManagement"""
        instance = ElementManagement.get_instance(self.db_module)
        self.assertIsInstance(instance, ElementManagement)

    def test_get_instance_returns_same_instance(self):
        """ Check that get_instance always returns the same instance of ElementManagement"""
        instance1 = ElementManagement.get_instance(self.db_module)
        instance2 = ElementManagement.get_instance(self.db_module)
        self.assertIs(instance1, instance2)

    def test_element_exists(self):
        """ Check that element_exists returns True if the element exists in the database """
        self.db_module.select_data = MagicMock(return_value={"_id": "id",
                                                                "title": "title",
                                                                "schedules": ["schedule1", "schedule2"],
                                                                "element_type": "event",
                                                                "start": "start",
                                                                "end": "end",
                                                                "description": "description"})
        result = self.element_management.element_exists("id")
        self.assertTrue(result)
        self.db_module.select_data.assert_called_with("elements", {"_id": "id"})

    def test_element_does_not_exist(self):
        """ Check that element_exists returns False if the element does not exist in the database """
        self.db_module.select_data = MagicMock(return_value=None)
        result = self.element_management.element_exists("id")
        self.assertFalse(result)
        self.db_module.select_data.assert_called_with("elements", {"_id": "id"})

    def test_update_id_exist(self):
        """ Check that update_id returns True if the element exists in the database """
        self.db_module.select_data = MagicMock(return_value={"_id": "id",
                                                "title": "title",
                                                "schedules": ["schedule1", "schedule2"],
                                                "element_type": "event",
                                                "start": "start",
                                                "end": "end",
                                                "description": "description"})

    def test_get_element_id_exists_on_dict(self):
        """ Check that get_element returns the element if it exists in the 
        dictionary """
        element = Mock(spec=Element)
        self.element_management.elements = {"id": element}
        result = self.element_management.get_element("id")
        self.assertEqual(result, element)

    # def test_get_element_id_exists_in_database(self):
    #     """ Check that get_element returns the element if it exists in the 
    #     database """
    #     element = Mock(spec=Element)
    #     self.db_module.select_data = MagicMock(return_value={"_id": "id",
    #                                             "title": "title",
    #                                             "schedules": ["schedule1", "schedule2"],
    #                                             "element_type": "event",
    #                                             "start": "start",
    #                                             "end": "end",
    #                                             "description": "description"})
    #     ElementFactory.create_element = MagicMock(return_value=element)
    #     result = self.element_management.get_element("id")
    #     self.assertEqual(result, element)
    #     self.assertEqual(self.element_management.elements["id"], element)

    def test_get_element_id_does_not_exist(self):
        """ Check that get_element raises ElementDoesNotExistError if the element 
        does not exist in the database """
        element = 'element'
        self.element_management.element_exists = MagicMock(return_value=False)
        with self.assertRaises(ElementDoesNotExistError):
            self.element_management.get_element(element)

    def test_update_element_id_exists(self):
        """ Check that update_element updates the element if it exists in the 
        database """
        element = Mock(spec=Element)
        self.element_management.elements = {"id": element}
        self.element_management.element_exists = MagicMock(return_value=True)
        self.element_management.update_element("id")
        element.to_dict.assert_called()

    def test_update_element_id_does_not_exist(self):
        """ Check that update_element raises ElementDoesNotExistError if the 
        element does not exist in the database """
        element = 'element'
        self.element_management.element_exists = MagicMock(return_value=False)
        with self.assertRaises(ElementDoesNotExistError):
            self.element_management.update_element(element)

    # def test_delete_element_id_exists(self):
    #     """ Check that delete_element deletes the element if it exists in the 
    #     database """
    #     element = Mock(spec=Element)
    #     self.element_management.elements = {"id": element}
    #     self.element_management.element_exists = MagicMock(return_value=True)
    #     self.element_management.delete_element("id")
    #     element.to_dict.assert_called()

    def test_delete_element_id_does_not_exist(self):
        """ Check that delete_element raises ElementDoesNotExistError if the 
        element does not exist in the database """
        element = 'element'
        self.element_management.element_exists = MagicMock(return_value=False)
        with self.assertRaises(ElementDoesNotExistError):
            self.element_management.delete_element(element)

    # def test_create_element_id_exists(self):
    #     """ Check that create_element raises ElementAlreadyExistsError if the 
    #     element already exists in the database """
    #     element = Mock(spec=Element)
    #     self.element_management.element_exists = MagicMock(return_value=True)
    #     with self.assertRaises(ElementAlreadyExistsError):
    #         self.element_management.create_element(element)

    # def test_create_element_id_does_not_exist(self):
    #     """ Check that create_element creates the element if it does not exist 
    #     in the database """
    #     element = Mock(spec=Element)
    #     self.element_management.element_exists = MagicMock(return_value=False)
    #     self.element_management.create_element(element)
    #     element.to_dict.assert_called()

    # def test_create_element_if_title_is_none(self):
    #     """ Check that create_element raises ValueError if title is None """
    #     element = Mock(spec=Element)
    #     element.title = None
    #     self.element_management.element_exists = MagicMock(return_value=False)
    #     with self.assertRaises(ValueError):
    #         self.element_management.create_element(element)

    def test_create_element_title_nonstring(self):
        """ Check that create_element raises TypeError if title is not a string """
        element = Mock(spec=Element)
        element.title = 1
        self.element_management.element_exists = MagicMock(return_value=False)
        with self.assertRaises(TypeError):
            self.element_management.create_element(element)

    # def test_create_element_if_schedules_is_none(self):
    #     """ Check that create_element raises ValueError if schedules is None """
    #     element = Mock(spec=Element)
    #     element.schedules = None
    #     self.element_management.element_exists = MagicMock(return_value=False)
    #     with self.assertRaises(ValueError):
    #         self.element_management.create_element(element)
    
    def test_create_element_schedules_nonlist(self):
        """ Check that create_element raises TypeError if schedules is not a list """
        element = Mock(spec=Element)
        element.schedules = 1
        self.element_management.element_exists = MagicMock(return_value=False)
        with self.assertRaises(TypeError):
            self.element_management.create_element(element)

    # def test_create_element_if_element_type_is_none(self):
    #     """ Check that create_element raises ValueError if element_type is None """
    #     element = Mock(spec=Element)
    #     element.element_type = None
    #     self.element_management.element_exists = MagicMock(return_value=False)
    #     with self.assertRaises(ValueError):
    #         self.element_management.create_element(element)

    def test_create_element_element_type_nonstring(self):
        """ Check that create_element raises TypeError if element_type is not a string """
        element = Mock(spec=Element)
        element.element_type = 1
        self.element_management.element_exists = MagicMock(return_value=False)
        with self.assertRaises(TypeError):
            self.element_management.create_element(element)
        

if __name__ == '__main__':
    unittest.main()
