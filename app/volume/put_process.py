from pulzarutils.utils import Utils
from pulzarutils.constants import ReqType
from pulzarutils.file_utils import FileUtils
from pulzarcore.core_request import CoreRequest
from pulzarcore.core_db import DB


class PutProcess:
    def __init__(self, constants):
        self.const = constants
        self.utils = Utils()
        self.db_backup = DB(self.const.DB_BACKUP)
        self.file_utils = FileUtils(self.const)
        self.complex_response = {
            'action': None,
            'parameters': None,
            'volume': None
        }

    def notify_record_to_master(self, env):
        """Report the register creation.
        """
        temporal = '-1'
        query_params = self.utils.extract_query_params(
            'http://fakeurl.com?'+env['QUERY_STRING'])
        if self.const.SET_TEMPORAL in query_params:
            temporal = query_params[self.const.SET_TEMPORAL][0]
        master_url = self.utils.extract_url_data(
            query_params['url'][0])
        # Confirming with master.
        req = CoreRequest(
            master_url['host'], master_url['port'], self.const.ADD_RECORD)
        req.set_type(ReqType.POST)
        req.set_path(self.const.ADD_RECORD)
        # We have to send the key, volume and port.
        req.set_payload({
            'key': self.file_utils.get_key(),
            'volume': env[self.const.HTTP_HOST],
            'temporal': temporal
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
            url_path, self.const.RE_PUT_VALUE)
        if regex_result:
            try:
                root_path, base_name = regex_result.groups()
                if root_path is None:
                    root_path = ''

                base64_str = self.utils.encode_base_64(
                    root_path + '/' + base_name, True)
                # Trying to create the key-value
                key_to_binary = self.utils.encode_str_to_byte(base64_str)
                self.file_utils.set_key(key_to_binary, base64_str)
                self.file_utils.set_path(root_path)
                key_generated = self.file_utils.read_binary_file(env)
                # Try to reach to master.
                if self.notify_record_to_master(env):
                    self.complex_response['action'] = self.const.KEY_ADDED
                else:
                    self.complex_response['action'] = self.const.KEY_ERROR

            except Exception as err:
                print('Error extracting key', err)
                self.complex_response['action'] = self.const.KEY_ERROR

        return self.complex_response
