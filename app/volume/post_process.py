from pulzarutils.utils import Utils
from pulzarutils.utils import Constants
from pulzarutils.constants import ReqType
from pulzarutils.file_utils import FileUtils
from pulzarcore.core_request import CoreRequest
from pulzarcore.core_db import DB


class PostProcess:
    def __init__(self):
        self.utils = Utils()
        self.db_backup = DB(Constants.DB_BACKUP)
        self.file_utils = FileUtils()
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
            master_url['host'], master_url['port'], Constants.ADD_RECORD)
        req.set_type(ReqType.POST)
        req.set_path(Constants.ADD_RECORD)
        # We have to send the key, volume and port.
        req.set_payload({
            'key': self.file_utils.key,
            'volume': env[Constants.HTTP_HOST]
        })
        if not req.make_request():
            # If an error ocurr in the server, we need to delete the file.
            self.file_utils.remove_file()
            return False
        try:
            self.db_backup.put_value(
                self.file_utils.key.encode(),
                b'1'
            )
        except Exception as err:
            print('notify_record_to_master', err)
        return True

    def process_request(self, env, start_response, url_path):
        regex_result = self.utils.get_search_regex(
            url_path, Constants.RE_PUT_VALUE)
        if regex_result:
            try:
                key_to_add = regex_result.groups()[0]
                base64_str = self.utils.encode_base_64(key_to_add, True)
                # Trying to create the key-value
                key_to_binary = self.utils.encode_str_to_byte(key_to_add)
                self.file_utils.set_key(key_to_binary, base64_str)
                key_generated = self.file_utils.read_binary_file(env)
                # Try to reach to master.
                if self.notify_record_to_master(env):
                    self.complex_response['action'] = Constants.KEY_ADDED
                else:
                    self.complex_response['action'] = Constants.KEY_ERROR

            except Exception as err:
                print('Error extracting key', err)
                self.complex_response['action'] = Constants.KEY_ERROR

        return self.complex_response
