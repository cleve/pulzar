from pulzarutils.utils import Utils
from pulzarutils.messenger import Messenger
from pulzarcore.core_db import DB


class GetProcess:
    def __init__(self, constants):
        self.const = constants
        self.utils = Utils()
        # DB of values already loaded
        self.db_values = DB(self.const.DB_PATH)
        self.messenger = Messenger()

    def process_request(self, env, start_response, url_path):
        """Entrance for get
        """
        # Get request type, checking for key value.
        regex_result = self.utils.get_search_regex(
            url_path, self.const.RE_GET_VALUE)

        if regex_result:
            try:
                root_path = ''
                raw_root_path, key = regex_result.groups()
                if raw_root_path is not None:
                    root_path = raw_root_path
                # Searching in the database
                key_to_binary = self.utils.encode_base_64(
                    root_path + '/' + key)
                # Getting volume,string_datetime
                composed_value = self.db_values.get_value(
                    key_to_binary, to_str=True)
                if composed_value is None:
                    self.messenger.http_code = '404 not found'
                    self.messenger.code_type = self.const.KEY_NOT_FOUND
                    self.messenger.mark_as_failed()
                    self.messenger.set_message = 'Volume not found'
                    return self.messenger
                # Extracting data.
                volume = composed_value.split(',')[0]
                self.messenger.http_code = '307 temporary redirect'
                self.messenger.code_type = self.const.KEY_FOUND
                self.messenger.volume = volume

            except Exception as err:
                print('Error Get process', err)
                self.messenger.code_type = self.const.PULZAR_ERROR
                self.messenger.mark_as_failed()
                self.messenger.set_message = str(err)

        else:
            self.messenger.code_type = self.const.USER_ERROR
            self.messenger.mark_as_failed()
            self.messenger.set_message = 'Wrong query'

        return self.messenger
