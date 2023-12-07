import unittest
from unittest import mock
from src.schedule.schedule_model import Schedule

class TestScheduleModel(unittest.TestCase):

    def setUp(self):
        # Set up for the tests
        self.id = "schedule_id"
        self.title = "schedule_title"
        self.description = "schedule_description"
        self.permissions = [("user_id1", "permission_type1"), 
                            ("user_id2", "permission_type2"),
                            ("user_id3", "permission_type1")]
        self.elements = ["element1", "element2"]

        self.schedule = Schedule(self.id, self.title, self.description, self.permissions, self.elements)

        # Access private attributes for testing
        self.schedule._Schedule__id = self.id
        self.schedule._Schedule__permissions = self.permissions
        self.schedule._Schedule__elements = self.elements

    def test_id_property(self):
        # Test the id property
        self.assertEqual(self.schedule.id, self.id)

    def test_permissions_property(self):
        # Test the permissions property
        self.assertEqual(self.schedule.permissions, self.permissions)

    def test_elements_property(self):
        # Test the elements property
        self.assertEqual(self.schedule.elements, self.elements)

    def test_set_title_valid(self):
        # Test setting a valid title
        valid_title = "Valid Title"
        self.schedule.set_title(valid_title)
        self.assertEqual(self.schedule.title, valid_title)

    def test_set_title_not_string(self):
        # Test setting a title that is not a string
        with self.assertRaises(TypeError):
            self.schedule.set_title(123)

    def test_set_title_none(self):
        # Test setting a title that is None
        with self.assertRaises(ValueError):
            self.schedule.set_title(None)

    def test_set_title_too_long(self):
        # Test setting a title that is too long
        with self.assertRaises(ValueError):
            self.schedule.set_title("a" * 51)
    
    def test_set_title_max_length(self):
        # Test setting a title that is exactly at the maximum length
        max_length_title = "a" * 50
        self.schedule.set_title(max_length_title)
        self.assertEqual(self.schedule.title, max_length_title)
    
    def test_set_title_whitespace(self):
        # Test setting a title that contains only whitespace
        with self.assertRaises(ValueError):
            self.schedule.set_title("   ")

    def test_set_title_empty(self):
        # Test setting an empty title
        with self.assertRaises(ValueError):
            self.schedule.set_title("")

    def test_set_description_valid(self):
        # Test setting a valid description
        valid_description = "Valid Description"
        self.schedule.set_description(valid_description)
        self.assertEqual(self.schedule.description, valid_description)

    def test_set_description_not_string(self):
        # Test setting a description that is not a string
        with self.assertRaises(TypeError):
            self.schedule.set_description(123)

    def test_set_description_none(self):
        # Test setting a description that is None
        self.schedule.set_description(None)
        self.assertEqual(self.schedule.description, None)

    def test_set_description_too_long(self):
        # Test setting a description that is too long
        with self.assertRaises(ValueError):
            self.schedule.set_description("a" * 501)

    def test_set_description_max_length(self):
        # Test setting a description that is exactly at the maximum length
        max_length_description = "a" * 500
        self.schedule.set_description(max_length_description)
        self.assertEqual(self.schedule.description, max_length_description)


if __name__ == '__main__':
    unittest.main()
