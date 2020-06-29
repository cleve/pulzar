from utils.utils import Utils
from core.core_db import DB


class AdminProcess:
    """Handle admin operations from manage
    """

    def __init__(self, constants):
        self.const = constants
        self.utils = Utils()
        # DB of values already loaded
        self.db_volumes = DB(self.const.DB_VOLUME)
        # Complex response, store the info necessary.
        self.complex_response = {
            'action': None,
            'parameters': None,
            'volume': None
        }
        self.mark_of_local_verification = b'varidb_execute_file_verification'

    def process_request(self, url_path):
        """Get request type, checking for key value.
        """
        regex_result = self.utils.get_search_regex(
            url_path, self.const.RE_ADMIN)
        if regex_result:
            try:
                self.complex_response['action'] = self.const.ADMIN
                call_path_list = regex_result.groups()[0].split('/')
                call_path_list = [x for x in call_path_list if x != '']
                # All nodes
                if len(call_path_list) == 1 and call_path_list[0] == 'start_backup':
                    db_backup = DB(self.const.DB_BACKUP)
                    db_backup.update_or_insert_value(
                        self.mark_of_local_verification, b'1')
                    self.complex_response['action'] = self.const.BACKUP_SCHEDULED
                return self.complex_response

            except Exception as err:
                print('Error processing requesgmt', err)
                return self.complex_response
        return self.complex_response
