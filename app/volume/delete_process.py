from pulzarutils.utils import Utils
from pulzarutils.utils import Constants
from pulzarutils.messenger import Messenger
from pulzarcore.core_db import DB
from pulzarutils.file_utils import FileUtils


class DeleteProcess:
    def __init__(self, logger):
        self.TAG = self.__class__.__name__
        self.logger = logger
        self.file_utils = FileUtils()
        self.utils = Utils()
        self.messenger = Messenger()

    def process_request(self, env, start_response, url_path):
        # Get request type, checking for key value.
        regex_result = self.utils.get_search_regex(
            url_path, Constants.RE_DELETE_VALUE)
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
                    self.messenger.code_type = Constants.KEY_NOT_FOUND
                    self.messenger.set_message = 'key not found'
                    self.messenger.mark_as_failed()
                elif self.file_utils.remove_file_with_path(full_path):
                    self.messenger.code_type = Constants.KEY_DELETED
                    self.messenger.set_message = 'key deleted'
                else:
                    self.messenger.code_type = Constants.KEY_NOT_FOUND
                    self.messenger.set_message = 'key not found'
                    self.messenger.mark_as_failed()

            except Exception as err:
                self.logger.exception(':{}:{}'.format(self.TAG, err))
                self.messenger.code_type = Constants.PULZAR_ERROR
                self.messenger.set_message = str(err)
                self.messenger.mark_as_failed()

        else:
            self.messenger.code_type = Constants.USER_ERROR
            self.messenger.set_message = 'wrong request'
            self.messenger.mark_as_failed()

        return self.messenger
