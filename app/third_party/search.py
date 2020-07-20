import json
import base64
import re
import datetime

# Public library from Vari
from utils.public import Public


class Search:
    """Search third party app:
        This class allow us to search by

        - key
        - dates

        Use:
            server/third_party/[key_to_search]?eq=mm-dd-yyyy&lt=mm-dd-yyyy&gt=mm-dd-yyyy

        eq has precedence.
    """

    def __init__(self, arg1, lt, gt, eq):
        self.arg1 = arg1
        self.less_than = lt
        self.greater_than = gt
        self.equal = eq
        self.public = Public()
        self.response = []
        # Used in the DB.
        self.date_format = '%Y-%m-%d-%H-%M-%S'

        self.date_configuration()

    def date_configuration(self):
        """Detemine precedence, if eq parameter is present
        will be the only parameter used
        """
        if self.equal is not None:
            self.less_than = None
            self.greater_than = None

    def get_key_date(self, datetime_string):
        """String to datetime object
        """
        return datetime.datetime.strptime(
            datetime_string, self.date_format).date()

    def do_the_work(self):
        """Method who actually do the search
        """
        for element in self.public.get_all_elements():
            key, val = element
            key_string = base64.b64decode(key).decode()
            if key_string.find(self.arg1) >= 0:
                val_decoded = val.decode().split(',')
                val_string = val_decoded[0]
                date_string = val_decoded[1]
                datetime_object = self.get_key_date(date_string)
                if self.less_than is not None and self.greater_than is not None:
                    if datetime_object > self.less_than and datetime_object < self.greater_than:
                        continue
                if self.less_than is not None and self.greater_than is None:
                    if datetime_object >= self.less_than:
                        continue
                if self.less_than is None and self.greater_than is not None:
                    if datetime_object <= self.greater_than:
                        continue
                if self.equal is not None:
                    if datetime_object != self.equal:
                        continue
                self.response.append({
                    'key': key_string,
                    'url': val_string + '/' + key_string
                })

    def json_return(self):
        """Json converter
        """
        return json.dumps({'results': self.response})


def execute(arguments, params):
    """Entrance point
    """
    datetime_expression = r'^(\d{1,2}-\d{1,2}-\d{4})$'
    expression = re.compile(datetime_expression)
    datetime_format = '%m-%d-%Y'
    less_than = None
    great_than = None
    equals = None
    # Check arguments
    if params:
        try:
            # less than
            if 'lt' in params:
                less_than = params['lt'][0]
                if expression.match(less_than) is None:
                    less_than = None
                else:
                    less_than = datetime.datetime.strptime(
                        less_than, datetime_format).date()

            # more than
            if 'gt' in params:
                great_than = params['gt'][0]
                if expression.match(great_than) is None:
                    great_than = None
                else:
                    great_than = datetime.datetime.strptime(
                        great_than, datetime_format).date()

            if 'eq' in params:
                equals = params['eq'][0]
                if expression.match(equals) is None:
                    equals = None
                else:
                    equals = datetime.datetime.strptime(
                        equals, datetime_format).date()
        except re.error as err:
            print(err)

    if len(arguments) == 0:
        return json.dumps({'err': 'no args detected'})
    search = Search(arguments[0], less_than, great_than, equals)
    search.do_the_work()
    return search.json_return()
