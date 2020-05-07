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
            url_path, self.const.RE_GET_VALUE)
        if regex_result:
            try:
                key_to_search = regex_result.groups()[0]
                # Searching in the database
                key_to_binary = self.utils.encode_base_64(key_to_search)
                value = self.db_values.get_value(key_to_binary)
                if value is None:
                    self.complex_response['action'] = self.const.KEY_NOT_FOUND 
                    return self.complex_response
                self.complex_response['action'] = self.const.KEY_FOUND
                self.complex_response['volume'] = value
                return self.complex_response

            except Exception as err:
                print('Error extracting key', err)
