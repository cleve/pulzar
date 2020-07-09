from utils.utils import Utils
from core.core_db import DB
import importlib


class TPProcess:
    def __init__(self, constants):
        self.const = constants
        self.utils = Utils()
        # DB of values already loaded
        self.db_values = DB(self.const.DB_PATH)
        # Complex response, store the info necessary.
        self.complex_response = {
            'action': None,
            'parameters': None,
            'volume': None
        }

    def process_request(self, url_path):
        # Get request type, checking for key value.
        regex_result = self.utils.get_search_regex(
            url_path, self.const.RE_THIRD_PARTY)
        if regex_result:
            try:
                call_path_list = regex_result.groups()[0][1:].split('/')
                file_name = call_path_list[0]
                args = call_path_list[1:]
                modules = self.utils.read_file_name_from_dir(
                    'third_party/', 'py')
                if file_name + '.py' in modules:
                    import_fly = importlib.import_module(
                        'third_party.' + file_name)
                    j_byte = import_fly.execute(args).encode()
                    self.complex_response['action'] = self.const.TP_RESPONSE
                    self.complex_response['parameters'] = j_byte

                return self.complex_response

            except Exception as err:
                print('Error third party', err)
