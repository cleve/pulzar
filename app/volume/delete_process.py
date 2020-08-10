from pulzarutils.utils import Utils
from pulzarcore.core_db import DB
from pulzarutils.file_utils import FileUtils


class DeleteProcess:
    def __init__(self, constants):
        self.const = constants
        self.file_utils = FileUtils(self.const)
        self.utils = Utils()
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
                root_path, base_name = regex_result.groups()
                if root_path is None:
                    root_path = ''
                # Searching in the database
                key_to_binary = self.utils.encode_base_64(
                    root_path + '/' + base_name)
                full_path = root_path + '/' + \
                    self.utils.decode_byte_to_str(key_to_binary)
                value = self.file_utils.is_value_present(full_path)
                if not value:
                    self.complex_response['action'] = self.const.KEY_NOT_FOUND
                    return self.complex_response
                if self.file_utils.remove_file_with_path(full_path):
                    self.complex_response['action'] = self.const.KEY_DELETED
                else:
                    self.complex_response['action'] = self.const.KEY_NOT_FOUND
                    self.complex_response['parameters'] = self.utils.decode_byte_to_str(
                        key_to_binary)
                return self.complex_response

            except Exception as err:
                print('Error extracting key', err)
