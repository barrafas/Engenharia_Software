import unittest
from datetime import datetime
from unittest.mock import Mock, MagicMock, patch
from src.calendar_elements.element_management import ElementManagement, ElementAlreadyExistsError, ElementDoesNotExistError
from src.calendar_elements.element_factory import ElementFactory
from src.database.mongo_module import MongoModule
from src.calendar_elements.element_interface import Element
from src.schedule.schedule_management import ScheduleManagement

class TestElementManagement(unittest.TestCase):
    """ Tests for ElementManagement class """
    def setUp(self):
        # Reset singleton instance and create a mock database module
        ElementManagement._instance = None
        self.db_module = Mock()
        self.elements = {'id': MagicMock(spec=Element)}
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

    def test_get_element_id_exists_on_dict(self):
        """ Check that get_element returns the element if it exists in the 
        dictionary """
        id_1 = "id"
        title = "title"
        schedules = ["schedule1", "schedule2"]
        element_type = "event"
        start = datetime(2021, 1, 1)
        end = datetime(2021, 1, 2)
        description = "description"
        element = ElementFactory.create_element(element_type, id_1, title, schedules, start=start, end=end, description=description)
        self.element_management.elements[id_1] = element
        result = self.element_management.get_element(id_1)
        self.assertEqual(result.title, title)


    def test_get_element_id_exists_in_database(self):
        """ Check that get_element returns the element if it exists in the 
        database """
        self.element_management.db_module.select_data = MagicMock(return_value={"_id": "id",
                                                "title": "title",
                                                "schedules": ["schedule1", "schedule2"],
                                                "element_type": "event",
                                                "start": datetime(2021, 1, 1),
                                                "end": datetime(2021, 1, 2),
                                                "description": "description"})
        self.element_management.element_exists = MagicMock(return_value=True)
        result = self.element_management.get_element("id")
        self.assertEqual(result.title, "title")
        self.assertEqual(result.schedules, ["schedule1", "schedule2"])
        self.assertEqual(result.element_type, "event")
        self.assertEqual(result.start, datetime(2021, 1, 1))
        self.assertEqual(result.end, datetime(2021, 1, 2))
        self.assertEqual(result.description, "description")

        
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
        element = Mock()
        self.element_management.elements = {"id": element}
        self.element_management.element_exists = MagicMock(return_value=True)
        self.element_management.update_element("id")
        element.to_dict.assert_called()

        # id_1 = "id"
        # title = "title"
        # schedules = ["schedule1", "schedule2"]
        # element_type = "event"
        # start = datetime(2021, 1, 1)
        # end = datetime(2021, 1, 2)
        # description = "description"
        # element = ElementFactory.create_element(element_type, id_1, title, 
        #                                         schedules = schedules,
        #                                         start=start, end=end, 
        #                                         description=description)
        # self.element_management.elements[id_1] = element
        # self.element_management.db_module.update_element = MagicMock()

        # self.element_management.db_module.update_data.assert_called_once_with("elements",
        #                                     {"_id": "id"}, element.to_dict())


    def test_update_element_id_does_not_exist(self):
        """ Check that update_element raises ElementDoesNotExistError if the 
        element does not exist in the database """
        element = 'id'
        self.element_management.element_exists = MagicMock(return_value=False)
        with self.assertRaises(ElementDoesNotExistError):
            self.element_management.update_element(element)

    # def test_delete_element_id_exists(self):
    #     """ Check that delete_element deletes the element if it exists in the 
    #     database """
    #     element_id = "id"
    #     self.element_management.db_module.delete_data = MagicMock()
    #     self.element_management.db_module.select_data.return_value = {"_id": element_id,
    #                                             "title": "title",
    #                                             "schedules": ["schedule1", "schedule2"],
    #                                             "element_type": "event",
    #                                             "start": datetime(2021, 1, 1),
    #                                             "end": datetime(2021, 1, 2),
    #                                             "description": "description"}
    #     self.element_management.delete_element(element_id)
    #     self.element_management.db_module.delete_data.assert_called_once_with("elements", {"_id": "id"})


    def test_delete_element_id_does_not_exist(self):
        """ Check that delete_element raises ElementDoesNotExistError if the 
        element does not exist in the database """
        element = 'element'
        self.element_management.element_exists = MagicMock(return_value=False)
        with self.assertRaises(ElementDoesNotExistError):
            self.element_management.delete_element(element)

    # def test_create_element(self):
    #     """ Check that create_element creates the element if it does not exist 
    #     in the database """
    #     self.db_module.insert_data = MagicMock()
    #     self.db_module.select_data = MagicMock(return_value=[])
    #     mock_schedule = Mock()
    #     with patch('Schedule', 'get_schedule' return_value=mock_schedule), \
    #         patch('src.calendar_elements.element_management.ElementFactory.create_element', return_value=Mock()):
    #         self.element_management.create_element("id", "title", ["schedule1", "schedule2"], "event", datetime(2021, 1, 1), datetime(2021, 1, 2), "description")

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
        # element = Mock(spec=Element)
        # self.element_management.element_exists = MagicMock(return_value=False)
        # self.element_management.create_element(element)
        # element.to_dict.assert_called()

    # def test_create_element_if_title_is_none(self):
    #     """ Check that create_element raises ValueError if title is None """
    #     element = Mock(spec=Element)
    #     element.title = None
    #     self.element_management.element_exists = MagicMock(return_value=False)
    #     with self.assertRaises(ValueError):
    #         self.element_management.create_element(element)

    # def test_create_element_title_nonstring(self):
    #     """ Check that create_element raises TypeError if title is not a string """
    #     element = Mock(spec=Element)
    #     element.title = 1
    #     self.element_management.element_exists = MagicMock(return_value=False)
    #     with self.assertRaises(TypeError):
    #         self.element_management.create_element(element)

    # def test_create_element_if_schedules_is_none(self):
    #     """ Check that create_element raises ValueError if schedules is None """
    #     element = Mock(spec=Element)
    #     element.schedules = None
    #     self.element_management.element_exists = MagicMock(return_value=False)
    #     with self.assertRaises(ValueError):
    #         self.element_management.create_element(element)
    
    # def test_create_element_schedules_nonlist(self):
    #     """ Check that create_element raises TypeError if schedules is not a list """
    #     element = Mock(spec=Element)
    #     element.schedules = 1
    #     self.element_management.element_exists = MagicMock(return_value=False)
    #     with self.assertRaises(TypeError):
    #         self.element_management.create_element(element)

    # def test_create_element_if_element_type_is_none(self):
    #     """ Check that create_element raises ValueError if element_type is None """
    #     element = Mock(spec=Element)
    #     element.element_type = None
    #     self.element_management.element_exists = MagicMock(return_value=False)
    #     with self.assertRaises(ValueError):
    #         self.element_management.create_element(element)

    # def test_create_element_element_type_nonstring(self):
    #     """ Check that create_element raises TypeError if element_type is not a string """
    #     element = Mock(spec=Element)
    #     element.element_type = 1
    #     self.element_management.element_exists = MagicMock(return_value=False)
    #     with self.assertRaises(TypeError):
    #         self.element_management.create_element(element)
        

if __name__ == '__main__':
    unittest.main()
