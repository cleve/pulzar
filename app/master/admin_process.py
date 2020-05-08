from utils.utils import Utils
from core.core_db import DB


class AdminProcess:
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

    def process_request(self, env, start_response, url_path):
        # Get request type, checking for key value.
        regex_result = self.utils.get_search_regex(
            url_path, self.const.RE_ADMIN)
        if regex_result:
            try:
                call_path_list = regex_result.groups()[0].split('/')
                call_path_list = [x for x in call_path_list if x != '']
                if len(call_path_list) == 1:
                    pass
                elif len(call_path_list) == 2:
                    pass
                
                self.complex_response['action'] = self.const.KEY_FOUND
                return self.complex_response

            except Exception as err:
                print('Error extracting key', err)
