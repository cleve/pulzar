from utils.utils import Utils
from utils.file_utils import FileUtils


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
                self.complex_response['action'] = self.const.NOTIFY_KEY_TO_MASTER
                self.complex_response['parameters'] = key_generated
                return self.complex_response

            except Exception as err:
                print('Error extracting key', err)
