from pulzarutils.utils import Utils
from pulzarutils.utils import Constants
from pulzarutils.messenger import Messenger
from pulzarcore.core_db import DB


class DeleteProcess:
    def __init__(self, logger):
        self.TAG = self.__class__.__name__
        self.logger = logger
        self.utils = Utils()
        # DB of values already loaded
        self.db_values = DB(Constants.DB_PATH)
        self.messenger = Messenger()

    def process_request(self, env, start_response, url_path):
        """Entrance for delete method

        Delete the key-value data from masterdb and redirect.
        """
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
                value = self.db_values.get_value(key_to_binary)
                if value is None:
                    self.messenger.code_type = Constants.KEY_NOT_FOUND
                    self.messenger.set_message = 'Value not found'
                    return self.messenger
                # Delete register on master.
                self.db_values.delete_value(key_to_binary)
                # Redirect to volume does not matter if was not deleted on master.
                value_string_volume = value.decode().split(',')[0]
                self.messenger.code_type = Constants.KEY_FOUND_DELETE
                self.messenger.volume = value_string_volume
                return self.messenger

            except Exception as err:
                self.logger.exception('{}:{}'.format(self.TAG, err))
                self.messenger.code_type = Constants.PULZAR_ERROR
                self.messenger.set_message = str(err)
                self.messenger.mark_as_failed()
                return self.messenger

        else:
            self.messenger.code_type = Constants.USER_ERROR
            self.messenger.mark_as_failed()
            self.messenger.set_message = 'Wrong query'
