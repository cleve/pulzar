import json


class Search:
    """Search third party app:
        This class allow us to search by

        - key
        - dates
    """

    def __init__(self, arg1):
        self.arg1 = arg1

    def do_the_work(self):
        """Method who actually do the search
        """
        print('Hello example with arg ', self.arg1)

    def json_return(self):
        """Json converter
        """
        return json.dumps({'my_arg': self.arg1})


def execute(arguments):
    """Entrance point
    """
    # Check arguments
    search = Search(arguments[0])
    search.do_the_work()
    return search.json_return()
