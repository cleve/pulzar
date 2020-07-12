from core.core_db import DB
from utils.constants import Constants


class Public:
    """Public class to be used for third parties
    """

    def __init__(self):
        self.const = Constants()

    def get_all_elements(self):
        """Get all the elements
            - return: Iterator
                elements are bytes of kind key, value

        """
        try:
            db_object = DB(self.const.DB_PATH)
            iterator = db_object.get_cursor_iterator()
            cursor = iterator.cursor()
            return cursor
        except Exception as err:
            raise('Public::' + str(err))

    def get_value(self, key):
        """Get the value associated to the key
            - args
                key (str): String to be searched

            - return
                dictionary or None if does not exist
                {
                    'value': [val],
                    'datetime': [datetime object]
                }
        """
        try:
            db_object = DB(self.const.DB_PATH)
            db_object.get_value(key, to_str=True)

        except Exception as err:
            return None

        return None
