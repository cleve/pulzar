from pulzarutils.utils import Utils
from pulzarutils.messenger import Messenger
from pulzarcore.core_db import DB


class PostProcess:
    """UNUSED CLASS"""

    def __init__(self, constants):
        self.const = constants
        # 20 mins max to consider a volume online.
        self.second_range = 1200
        self.utils = Utils()
        # DB of values already loaded.
        self.db_values = DB(self.const.DB_PATH)
        # DB of volumes/keys.
        self.db_volumes = DB(self.const.DB_VOLUME)
        self.messenger = Messenger()
        # Complex response, store the info necessary.
        self.complex_response = {
            'action': None,
            'parameters': None,
            'volume': None
        }

    def pick_a_volume(self):
        volumes = self.db_volumes.get_keys_values()
        current_datetime = self.utils.get_current_datetime()
        min_value = 100
        server = None
        for elem in volumes:
            # meta_raw[0] = precent, meta_raw[1] = load
            meta_raw = self.utils.decode_byte_to_str(elem[1]).split(':')
            percent = int(meta_raw[0])
            last_update_reported = self.utils.get_datetime_from_string(
                meta_raw[3])
            delta_time = current_datetime - last_update_reported
            # Check availability of node.
            if delta_time.total_seconds() >= self.second_range:
                continue
            if percent < min_value:
                min_value = percent
                server = elem[0]
        return server

    def process_request(self, env, start_response, url_path):
        regex_result = self.utils.get_search_regex(
            url_path, self.const.RE_POST_VALUE)
        if regex_result:
            try:
                key_to_add = regex_result.groups()[0]
                # Searching in the database
                key_to_binary = self.utils.encode_str_to_byte(key_to_add)
                value = self.db_values.get_value(key_to_binary)
                # If not, we will try to create the entry process.
                if value is None:
                    volume = self.pick_a_volume()
                    # Populating dictionary with the info needed.
                    self.complex_response['action'] = self.const.REDIRECT_POST
                    self.complex_response['parameters'] = key_to_binary
                    self.complex_response['volume'] = volume
                    return self.complex_response
                # Since key was found, an element was already added before
                # using the same key.
                self.complex_response['action'] = self.const.KEY_ALREADY_ADDED
                return self.complex_response

            except Exception as err:
                print('Error extracting key', err)
