from pulzarutils.utils import Utils
from pulzarutils.utils import Constants
from pulzarutils.messenger import Messenger
from pulzarcore.core_db import DB


class AdminProcess:
    """Handle admin operations from manage
    """

    def __init__(self, logger):
        self.TAG = self.__class__.__name__
        self.logger = logger
        self.utils = Utils()
        self.messenger = Messenger()
        self.mark_of_local_verification = b'varidb_execute_file_verification'

    def process_request(self, url_path):
        """Get request type, checking for key value.
        """
        regex_result = self.utils.get_search_regex(
            url_path, Constants.RE_ADMIN)
        if regex_result:
            try:
                call_path_list = regex_result.groups()[0].split('/')
                call_path_list = [x for x in call_path_list if x != '']
                # All nodes
                if len(call_path_list) == 1 and call_path_list[0] == 'start_backup':
                    db_backup = DB(Constants.DB_BACKUP)
                    db_backup.update_or_insert_value(
                        self.mark_of_local_verification, b'1')
                    self.messenger.code_type = Constants.BACKUP_SCHEDULED
                    self.messenger.set_message = 'backup scheduled'

            except Exception as err:
                self.logger.exception('{}:{}'.format(self.TAG, err))
                self.messenger.code_type = Constants.PULZAR_ERROR
                self.messenger.set_message = str(err)
                self.messenger.mark_as_failed()
        else:
            self.messenger.code_type = Constants.USER_ERROR
            self.messenger.set_message = 'wrong request'
            self.messenger.mark_as_failed()

        return self.messenger
