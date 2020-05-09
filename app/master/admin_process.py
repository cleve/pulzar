from utils.utils import Utils
from core.core_db import DB


class AdminProcess:
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

    def process_request(self, env, start_response, url_path):
        # Get request type, checking for key value.
        regex_result = self.utils.get_search_regex(
            url_path, self.const.RE_ADMIN)
        if regex_result:
            try:
                self.complex_response['action'] = self.const.ADMIN
                call_path_list = regex_result.groups()[0].split('/')
                call_path_list = [x for x in call_path_list if x != '']
                # All nodes
                if len(call_path_list) == 1 and call_path_list[0] == 'network':
                    nodes = self.db_volumes.get_keys_values(to_str=True)
                    self.complex_response['parameters'] = self.utils.py_to_json([{'node': n[0], 'percent':int(n[1])} for n in nodes], to_bin=True)
                    
                elif len(call_path_list) == 2 and call_path_list[0] == 'network':
                    node_to_search = self.utils.encode_str_to_byte(call_path_list[1])
                    get_result = {'percent': self.db_volumes.get_value(node_to_search, to_str=True)}
                    self.complex_response['parameters'] = self.utils.py_to_json(get_result, to_bin=True)
                
                else:
                    self.complex_response['action'] = self.const.KEY_NOT_FOUND
                return self.complex_response

            except Exception as err:
                print('Error extracting key', err)
