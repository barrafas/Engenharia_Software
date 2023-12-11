import unittest
from datetime import datetime
from unittest.mock import Mock, MagicMock, patch
from src.calendar_elements.element_management import ElementManagement, ElementAlreadyExistsError, ElementDoesNotExistError
from src.calendar_elements.element_factory import ElementFactory
from src.database.mongo_module import MongoModule
from src.calendar_elements.element_interface import Element
# from src.schedule.schedule_management import ScheduleManagement

class TestElementManagement(unittest.TestCase):
    """ Tests for ElementManagement class """
    def setUp(self):
        # Reset singleton instance and create a mock database module
        ElementManagement._instance = None
        self.db_module = MagicMock()
        self.elements = {'id': MagicMock(spec=Element)}
        self.element_management = ElementManagement.get_instance(self.db_module)

        from src.schedule.schedule_management import ScheduleManagement
        ScheduleManagement._instance = None
        self.schedule_management = ScheduleManagement.get_instance(self.db_module)

        from src.user.user_management import UserManagement
        UserManagement._instance = None
        self.user_management = UserManagement.get_instance(self.db_module)

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
        self.assertEqual(result.schedules, schedules)
        self.assertEqual(result.element_type, element_type)
        self.assertEqual(result.start, start)
        self.assertEqual(result.end, end)
        self.assertEqual(result.description, description)


    def test_get_element_id_exists_in_database(self):
        """ Check that get_element returns the element if it exists in the 
        database """
        self.element_management.db_module.select_data = MagicMock(return_value=[{"_id": "id",
                                                "title": "title",
                                                "schedules": ["schedule1", "schedule2"],
                                                "element_type": "event",
                                                "start": datetime(2021, 1, 1),
                                                "end": datetime(2021, 1, 2),
                                                "description": "description"}])
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
        # self.element_management.db_module.update_data = MagicMock()
        # print('AAAAAAAAAA')
        # self.element_management.update_element(id_1)
        # print('BBBBBBBBBB')
        # self.element_management.db_module.update_data.assert_called_once_with("elements", {"_id": "id"}, element.to_dict())


    def test_update_element_id_does_not_exist(self):
        """ Check that update_element raises ElementDoesNotExistError if the 
        element does not exist in the database """
        element = 'id'
        self.element_management.element_exists = MagicMock(return_value=False)
        with self.assertRaises(ElementDoesNotExistError):
            self.element_management.update_element(element)

    def test_delete_element_id_exists(self):
        """ Check that delete_element deletes the element if it exists in the 
        database """
        element_id = "id"
        self.element_management.db_module.delete_data = MagicMock()
        def mock_select_data(collection, query):
            if collection == "elements" and query == {"_id": "id"}:
                return [{"_id": "id",
                        "title": "title",
                        "schedules": ["schedule1", "schedule2"],
                        "element_type": "event",
                        "start": datetime(2021, 1, 1),
                        "end": datetime(2021, 1, 2),
                        "description": "description"}]
            if collection == "schedules" and query == {"_id": "schedule1"}:
                return [{"_id": "schedule1",
                        "title": "title1",
                        "description": "description",
                        "permissions": {"user1": 'owner', "user2": "editor"},
                        "elements": ["id", "element2"]}]
            if collection == "schedules" and query == {"_id": "schedule2"}:
                return [{"_id": "schedule2",
                        "title": "title2",
                        "description": "description",
                        "permissions": {"user1": 'owner', "user2": "editor"},
                        "elements": ["id"]}]
                        
        self.element_management.db_module.select_data = MagicMock(side_effect=mock_select_data)
        self.element_management.delete_element(element_id)
        self.element_management.db_module.delete_data.assert_called_once_with("elements", {"_id": "id"})


    def test_delete_element_id_does_not_exist(self):
        """ Check that delete_element raises ElementDoesNotExistError if the 
        element does not exist in the database """
        element = 'element'
        self.element_management.element_exists = MagicMock(return_value=False)
        with self.assertRaises(ElementDoesNotExistError):
            self.element_management.delete_element(element)

    def test_create_element(self):
        """ Check that create_element creates the element if it does not exist 
        in the database """
        self.element_management.db_module.delete_data = MagicMock()
        def mock_select_data(collection, query):
            if collection == "elements" and query == {"_id": "id"}:
                return [{"_id": "id",
                        "title": "title",
                        "schedules": ["schedule1", "schedule2"],
                        "element_type": "event",
                        "start": datetime(2021, 1, 1),
                        "end": datetime(2021, 1, 2),
                        "description": "description"}]
            if collection == "schedules" and query == {"_id": "schedule1"}:
                return [{"_id": "schedule1",
                        "title": "title1",
                        "description": "description",
                        "permissions": {"user1": 'owner', "user2": "editor"},
                        "elements": ["id", "element2"]}]
            if collection == "schedules" and query == {"_id": "schedule2"}:
                return [{"_id": "schedule2",
                        "title": "title2",
                        "description": "description",
                        "permissions": {"user1": 'owner', "user2": "editor"},
                        "elements": ["id"]}]
        self.element_management.db_module.select_data = MagicMock(side_effect=mock_select_data)
        self.element_management.db_module.insert_data = MagicMock()
        element_id = "id"
        title = "title"
        schedules = ["schedule1", "schedule2"]
        element_type = "event"
        start = datetime(2021, 1, 1)
        end = datetime(2021, 1, 2)
        description = "description"
        element = ElementFactory.create_element(element_type, element_id, title, schedules, start=start, end=end, description=description)
        self.element_management.element_exists = MagicMock(return_value=False)
        self.element_management.create_element(element_type = element_type, element_id = element_id, title = title, schedules = schedules, start=start, end=end, description=description)
        self.db_module.insert_data.assert_called_once_with("elements", element.to_dict())

    def test_create_element_id_exists(self):
        """ Check that create_element raises ElementAlreadyExistsError if the 
        element already exists in the database """
        element_id = "id"
        title = "title"
        schedules = ["schedule1", "schedule2"]
        element_type = "event"
        start = datetime(2021, 1, 1)
        end = datetime(2021, 1, 2)
        description = "description"
        self.element_management.element_exists = MagicMock(return_value=True)
        with self.assertRaises(ElementAlreadyExistsError):
            self.element_management.create_element(element_type, element_id, title, schedules, start=start, end=end, description=description)

    def test_create_element_invalid_element_type(self):
        """ Check that create_element raises ValueError if the element type is 
        invalid """
        element_id = "id"
        title = "title"
        schedules = ["schedule1", "schedule2"]
        element_type = "invalid_element_type"
        start = datetime(2021, 1, 1)
        end = datetime(2021, 1, 2)
        description = "description"
        with self.assertRaises(ValueError):
            self.element_management.create_element(element_type, element_id, title, schedules, start=start, end=end, description=description)

    def test_create_element_invalid_element_id(self):
        """ Check that create_element raises TypeError if the element id is 
        invalid """
        element_id = 1
        title = "title"
        schedules = ["schedule1", "schedule2"]
        element_type = "event"
        start = datetime(2021, 1, 1)
        end = datetime(2021, 1, 2)
        description = "description"
        with self.assertRaises(TypeError):
            self.element_management.create_element(element_type, element_id, title, schedules, start=start, end=end, description=description)
    
    def test_create_element_invalid_title(self):
        """ Check that create_element raises TypeError if the title is invalid """
        element_id = "id"
        title = 1
        schedules = ["schedule1", "schedule2"]
        element_type = "event"
        start = datetime(2021, 1, 1)
        end = datetime(2021, 1, 2)
        description = "description"
        with self.assertRaises(TypeError):
            self.element_management.create_element(element_type, element_id, title, schedules, start=start, end=end, description=description)

    def test_create_element_invalid_schedules(self):
        """ Check that create_element raises ValueError if the schedules are 
        invalid """
        element_id = "id"
        title = "title"
        schedules = "invalid_schedules"
        element_type = "event"
        start = datetime(2021, 1, 1)
        end = datetime(2021, 1, 2)
        description = "description"
        with self.assertRaises(TypeError):
            self.element_management.create_element(element_type, element_id, title, schedules, start=start, end=end, description=description)

    def test_create_element_invalid_schedules2(self):
        """ Check that create_element raises ValueError if the schedules are 
        invalid """
        element_id = "id"
        title = "title"
        schedules = [1, 2]
        element_type = "event"
        start = datetime(2021, 1, 1)
        end = datetime(2021, 1, 2)
        description = "description"
        with self.assertRaises(TypeError):
            self.element_management.create_element(element_type, element_id, title, schedules, start=start, end=end, description=description)

    def test_create_element_invalid_schedules3(self):
        """ Check that create_element raises TypeError if the schedules are 
        invalid """
        element_id = "id"
        title = "title"
        schedules = []
        element_type = "event"
        start = datetime(2021, 1, 1)
        end = datetime(2021, 1, 2)
        description = "description"
        with self.assertRaises(ValueError):
            self.element_management.create_element(element_type, element_id, title, schedules, start=start, end=end, description=description)

if __name__ == '__main__':
    unittest.main()
