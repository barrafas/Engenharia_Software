""" Export module for database """
import pandas as pd

from src.user.user_management import UserManagement

class ExportModule():
    """ Export module for database

    Attributes:
        db (DatabaseModule): The DatabaseModule object.
    
    Methods:
        export_data: Export data from database to csv file.
    """
    def __init__(self, db):
        """ Export module for database

        Attributes:
            db (DatabaseModule): The DatabaseModule object.

        Methods:
            export_data: Export data from database to csv file.
        """
        self.db = db

    def export_data(self, user_id):
        """ Export data from database to csv file """
        user_management = UserManagement.get_instance()

        user = user_management.get_user(user_id)

        elements = user.get_elements()

        elements_dict = []

        for element in elements:
            elements_dict.append(element.to_dict())

        df = pd.DataFrame(elements_dict)

        df.to_csv(f'exported_data_{user_id}.csv', index=False)

