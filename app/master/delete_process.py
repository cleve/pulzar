from pulzarutils.utils import Utils
from pulzarutils.messenger import Messenger
from pulzarcore.core_db import DB


class DeleteProcess:
    def __init__(self, constants, logger):
        self.TAG = self.__class__.__name__
        self.logger = logger
        self.const = constants
        self.utils = Utils()
        # DB of values already loaded
        self.db_values = DB(self.const.DB_PATH)
        self.messenger = Messenger()

    def process_request(self, env, start_response, url_path):
        """Entrance for delete method
        """
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
                value = self.db_values.get_value(key_to_binary)
                if value is None:
                    self.messenger.code_type = self.const.KEY_NOT_FOUND
                    self.messenger.set_message = 'Value not found'
                    return self.messenger
                # Delete register on master.
                self.db_values.delete_value(key_to_binary)
                # Redirect to volume does not matter if was not deleted on master.
                value_string_volume = value.decode().split(',')[0]
                self.messenger.code_type = self.const.KEY_FOUND_DELETE
                self.messenger.volume = value_string_volume
                return self.messenger

            except Exception as err:
                self.logger.exception('{}:{}'.format(self.TAG, err))
                self.messenger.code_type = self.const.PULZAR_ERROR
                self.messenger.set_message = str(err)
                self.messenger.mark_as_failed()
                return self.messenger

        else:
            self.messenger.code_type = self.const.USER_ERROR
            self.messenger.mark_as_failed()
            self.messenger.set_message = 'Wrong query'
