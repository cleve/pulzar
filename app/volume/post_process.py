from utils.utils import Utils
from utils.constants import ReqType
from utils.file_utils import FileUtils
from core.core_request import CoreRequest


class PostProcess:
    def __init__(self, constants):
        self.const = constants
        self.utils = Utils()
        self.file_utils = FileUtils(self.const)
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
        # We have to send the key.
        req.set_payload(self.file_utils.key)
        if not req.make_request():
            # If an error ocurr in the server, we need to delete the file.
            self.file_utils.remove_file()
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
                self.file_utils.set_key(key_to_binary, base64_str)
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
