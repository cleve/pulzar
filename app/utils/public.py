from core.core_db import DB
from utils.constants import Constants


class Public:
    """Public class to be used for third parties
    """

    def __init__(self):
        self.const = Constants()

    def get_all_elements(self):
        """Get all the elements
            This is an iterator
        """
        try:
            db_object = DB(self.const.DB_PATH)
            return db_object.get_cursor_iterator()
        except Exception as err:
            return None

    def get_value(self, key):
        """Get the value associated to the key
            - args
                key (str): String to be searched

            - return
                string with the value or None if does not exist
        """
        return None
