from pulzarutils.utils import Utils
from pulzarutils.messenger import Messenger
from pulzarcore.core_db import DB
from pulzarcore.core_rdb import RDB


class AdminProcess:
    def __init__(self, constants):
        self.const = constants
        self.utils = Utils()
        # DB of values already loaded
        self.db_volumes = DB(self.const.DB_VOLUME)
        self.messenger = Messenger()

    def process_request(self, url_path):
        """Entrance for Admin
        :param url_path:
        """
        # Get request type, checking for key value.
        regex_result = self.utils.get_search_regex(
            url_path, self.const.RE_ADMIN)
        if regex_result:
            try:
                self.messenger.code_type = self.const.ADMIN
                call_path_list = regex_result.groups()[0].split('/')
                call_path_list = [x for x in call_path_list if x != '']
                # All node status
                if len(call_path_list) == 1 and call_path_list[0] == 'network':
                    nodes_info = []
                    nodes = self.db_volumes.get_keys_values(to_str=True)
                    current_datetime = self.utils.get_current_datetime()
                    if len(nodes) == 0:
                        self.messenger.set_message = 'No nodes online'
                    for node in nodes:
                        node_name = node[0]
                        raw_split_info = node[1].split(':')
                        node_datetime = self.utils.get_datetime_from_string(
                            raw_split_info[3])
                        delta_t = current_datetime - node_datetime
                        nodes_info.append(
                            {
                                'node': node_name,
                                'percent': raw_split_info[0],
                                'load': raw_split_info[1],
                                'synch': True if delta_t.total_seconds() < 1200 else False
                            }
                        )

                    self.messenger.set_response(nodes_info)

                # Node status
                elif len(call_path_list) == 2 and call_path_list[0] == 'network':
                    node_to_search = self.utils.encode_str_to_byte(
                        call_path_list[1])
                    node = self.db_volumes.get_value(
                        node_to_search, to_str=True)
                    current_datetime = self.utils.get_current_datetime()
                    raw_split_info = node.split(':')
                    node_datetime = self.utils.get_datetime_from_string(
                        raw_split_info[3])
                    delta_t = current_datetime - node_datetime
                    get_result = {
                        'percent': raw_split_info[0],
                        'load': raw_split_info[1],
                        'synch': True if delta_t.total_seconds() < 1200 else False
                    }
                    self.messenger.set_response(get_result)

                elif len(call_path_list) == 1 and call_path_list[0] == 'status':
                    db_master = DB(self.const.DB_PATH)
                    self.messenger.set_response(db_master.get_stats())
                else:
                    self.messenger.code_type = self.const.KEY_NOT_FOUND
                    self.messenger.mark_as_failed()
                return self.messenger

            except Exception as err:
                print('Error extracting key', err)
                self.messenger.code_type = self.const.PULZAR_ERROR
                self.messenger.set_message = str(err)
                self.messenger.mark_as_failed()
                return self.messenger
