import json
import base64

from utils.public import Public


class Search:
    """Search third party app:
        This class allow us to search by

        - key
        - dates
    """

    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.public = Public()
        self.response = []

    def do_the_work(self):
        """Method who actually do the search
        """
        for element in self.public.get_all_elements():
            key, val = element
            key_string = base64.b64decode(key).decode()
            if key_string.find(self.arg1) >= 0:
                val_string = val.decode().split(',')[0]
                self.response.append({
                    'key': key_string,
                    'url': val_string + '/' + key_string
                })

    def json_return(self):
        """Json converter
        """
        return json.dumps({'results': self.response})


def execute(arguments):
    """Entrance point
    """
    # Check arguments
    search = Search(arguments[0], arguments[1])
    search.do_the_work()
    return search.json_return()
