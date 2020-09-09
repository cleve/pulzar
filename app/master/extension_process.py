import importlib
from pulzarutils.utils import Utils
from pulzarcore.core_body import Body
from pulzarcore.core_db import DB
from pulzarutils.messenger import Messenger


class ExtensionProcess:
    """Process extension calls
    """

    def __init__(self, constants):
        self.const = constants
        self.utils = Utils()
        # DB of values already loaded
        self.db_values = DB(self.const.DB_PATH)
        self.messenger = Messenger()

    def process_request(self, url_path, query_string):
        # Extract query parameters if is the case
        query_params = self.utils.extract_query_params(
            'http://fakeurl.com?' + query_string)
        # Get request type, checking for key value.
        regex_result = self.utils.get_search_regex(
            url_path, self.const.RE_EXTENSION)
        if regex_result:
            try:
                call_path_list = regex_result.groups()[0][1:].split('/')
                file_name = call_path_list[0]
                args = call_path_list[1:]
                modules = self.utils.read_file_name_from_dir(
                    'extensions/', 'py')
                if file_name + '.py' in modules:
                    import_fly = importlib.import_module(
                        'extensions.' + file_name)
                    j_byte = import_fly.execute(args, query_params)
                    self.messenger.code_type = self.const.EXTENSION_RESPONSE
                    self.messenger.set_response(j_byte)
                else:
                    self.messenger.code_type = self.const.USER_ERROR
                    self.messenger.mark_as_failed()
                    self.messenger.set_message = 'Wrong query, extension not found'

            except Exception as err:
                print('Error extension', err)
                self.messenger.code_type = self.const.PULZAR_ERROR
                self.messenger.mark_as_failed()
                self.messenger.set_message = str(msg)

        else:
            self.messenger.code_type = self.const.USER_ERROR
            self.messenger.mark_as_failed()
            self.messenger.set_message = 'Wrong query'

        return self.messenger
