from pulzarutils.utils import Utils
from pulzarutils.messenger import Messenger
from pulzarcore.core_db import DB
from pulzarutils.file_utils import FileUtils


class GetProcess:
    def __init__(self, constants):
        self.const = constants
        self.file_utils = FileUtils(self.const)
        self.utils = Utils()
        self.messenger = Messenger()

    def process_request(self, env, start_response, url_path):
        # Get request type, checking for key value.
        regex_result = self.utils.get_search_regex(
            url_path, self.const.RE_GET_VALUE)
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
                    self.messenger.http_code = '404 not found'
                    self.messenger.code_type = self.const.KEY_NOT_FOUND
                    self.messenger.set_message = 'key not found'
                    self.messenger.mark_as_failed()
                else:
                    self.messenger.code_type = self.const.KEY_FOUND
                    self.messenger.extra = full_path

            except Exception as err:
                print('Error GetProcess', err)
                self.messenger.code_type = self.const.PULZAR_ERROR
                self.messenger.set_message = str(err)
                self.messenger.mark_as_failed()

        else:
            self.messenger.code_type = self.const.USER_ERROR
            self.messenger.set_message = 'wrong request'
            self.messenger.mark_as_failed()

        return self.messenger
