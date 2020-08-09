from pulzarutils.utils import Utils
from pulzarcore.core_db import DB


class DeleteProcess:
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
            url_path, self.const.RE_DELETE_VALUE)
        if regex_result:
            try:
                key_to_search = regex_result.groups()[0]
                # Searching in the database
                key_to_binary = self.utils.encode_base_64(key_to_search)
                value = self.db_values.get_value(key_to_binary)
                if value is None:
                    self.complex_response['action'] = self.const.KEY_NOT_FOUND
                    return self.complex_response
                # Delete register on master.
                self.db_values.delete_value(key_to_binary)
                # Redirect to volume does not matter if was not deleted on master.
                value_string_volume = value.decode().split(',')[0]
                self.complex_response['action'] = self.const.KEY_FOUND_DELETE
                self.complex_response['volume'] = value_string_volume
                return self.complex_response

            except Exception as err:
                print('Error extracting key', err)
