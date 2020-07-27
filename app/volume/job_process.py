from utils.utils import Utils
from utils.constants import ReqType
from utils.node_utils import NodeUtils
from core.core_request import CoreRequest
from core.core_db import DB
from core.core_job import Job


class JobProcess:
    """Main class to handle jobs
    """

    def __init__(self, constants):
        self.const = constants
        self.utils = Utils()
        self.db_backup = DB(self.const.DB_BACKUP)
        self.complex_response = {
            'action': None,
            'parameters': None,
            'volume': None
        }

    def notify_record_to_master(self, env):
        # Report the register creation.
        master_url = self.utils.extract_url_data(
            env['QUERY_STRING'])
        # Confirming with master.
        req = CoreRequest(
            master_url['host'], master_url['port'], self.const.ADD_RECORD)
        req.set_type(ReqType.POST)
        req.set_path(self.const.ADD_RECORD)
        # We have to send the key, volume and port.
        req.set_payload({
            'key': 'self.file_utils.key',
            'volume': env[self.const.HTTP_HOST]
        })
        if not req.make_request():
            # If an error ocurr in the server, we need to delete the file.

            return False

        return True

    def process_request(self, env, start_response, url_path):
        regex_result = self.utils.get_search_regex(
            url_path, self.const.RE_POST_VALUE)
        if regex_result:
            try:
                key_to_add = regex_result.groups()[0]
                base64_str = self.utils.encode_base_64(key_to_add, True)
                # Trying to create the key-value
                key_to_binary = self.utils.encode_str_to_byte(key_to_add)

                # Try to reach to master.
                if self.notify_record_to_master(env):
                    self.complex_response['action'] = self.const.KEY_ADDED
                else:
                    self.complex_response['action'] = self.const.KEY_ERROR

            except Exception as err:
                print('Error extracting key', err)
                self.complex_response['action'] = self.const.KEY_ERROR

        return self.complex_response
