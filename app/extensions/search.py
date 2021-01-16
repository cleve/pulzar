import json
import base64
import re
import datetime
from pulzarutils.extension import Extension

# Public library
from pulzarutils.public import Public


class Search(Extension):
    """Search third party app:
        This class allow us to search by

        - key
        - dates

        Use:
            server/extension/[key_to_search]?eq=mm-dd-yyyy&lt=mm-dd-yyyy&gt=mm-dd-yyyy

        eq has precedence.
    """

    def __init__(self, arguments, params, file_path=None):
        self.args = arguments
        self.params = params
        self.public = Public()
        self.response = []
        # Used in the DB.
        self.date_format = '%Y-%m-%d-%H-%M-%S'

    def set_up(self):
        '''Configure params
        '''
        datetime_expression = r'^(\d{1,2}-\d{1,2}-\d{4})$'
        expression = re.compile(datetime_expression)
        datetime_format = '%m-%d-%Y'
        less_than = None
        great_than = None
        equals = None
        limit = None
        # Check arguments
        if self.params:
            try:
                # limit the search
                if 'limit' in self.params:
                    limit = int(self.params['limit'][0])
                # less than
                if 'lt' in self.params:
                    less_than = self.params['lt'][0]
                    if expression.match(less_than) is None:
                        less_than = None
                    else:
                        less_than = datetime.datetime.strptime(
                            less_than, datetime_format).date()

                # greater than
                if 'gt' in self.params:
                    great_than = self.params['gt'][0]
                    if expression.match(great_than) is None:
                        great_than = None
                    else:
                        great_than = datetime.datetime.strptime(
                            great_than, datetime_format).date()

                if 'eq' in self.params:
                    equals = self.params['eq'][0]
                    if expression.match(equals) is None:
                        equals = None
                    else:
                        equals = datetime.datetime.strptime(
                            equals, datetime_format).date()
            except re.error as err:
                print(err)

        self.less_than = less_than
        self.greater_than = great_than
        self.equal = equals
        self.limit = limit

        if len(self.args) == 0:
            return json.dumps({'err': 'no args detected'})
        self.search = self.args[0]
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
        records = 0
        for element in self.public.get_all_elements():
            # Limit the response since filed.
            print(records, self.limit)
            if self.limit is not None and records >= self.limit:
                return self.response
            key, val = element
            key_string = base64.b64decode(key).decode()
            if key_string.find(self.search) >= 0:
                val_decoded = val.decode().split(',')
                val_string = val_decoded[0]
                date_string = val_decoded[1]
                datetime_object = self.get_key_date(date_string)
                if self.less_than is not None and self.greater_than is not None:
                    if datetime_object >= self.greater_than and datetime_object <= self.less_than:
                        self.response.append({
                            'key': key_string,
                            'url': 'http://' + val_string + '/get_key' + key_string
                        })
                        records += 1

                elif self.less_than is not None and self.greater_than is None:
                    if datetime_object <= self.less_than:
                        self.response.append({
                            'key': key_string,
                            'url': 'http://' + val_string + '/get_key' + key_string
                        })
                        records += 1
                elif self.less_than is None and self.greater_than is not None:
                    if datetime_object >= self.greater_than:
                        self.response.append({
                            'key': key_string,
                            'url': 'http://' + val_string + '/get_key' + key_string
                        })
                        records += 1
                elif self.equal is not None:
                    if datetime_object == self.equal:
                        self.response.append({
                            'key': key_string,
                            'url': 'http://' + val_string + '/get_key' + key_string
                        })
                        records += 1
                else:
                    self.response.append({
                        'key': key_string,
                        'url': 'http://' + val_string + '/get_key' + key_string
                    })
                    records += 1

    def get_response(self):
        """Get the final object
        """
        return self.response

    def execute(self):
        """Entrance point
        """
        self.set_up()
        self.do_the_work()
        return self.get_response()
