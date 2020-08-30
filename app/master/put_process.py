from pulzarutils.utils import Utils
from pulzarutils.stream import Config
from pulzarutils.messenger import Messenger
from pulzarcore.core_db import DB


class PutProcess:
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

    def pick_a_volume(self):
        # Selecting port
        config = Config(self.const.CONF_PATH)
        volume_port = config.get_config('volume', 'port')
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
        if server is None:
            return None
        return server.decode() + ':' + volume_port

    def process_request(self, env, start_response, url_path):
        regex_result = self.utils.get_search_regex(
            url_path, self.const.RE_PUT_VALUE)

        if regex_result:
            try:
                raw_root_path, key_to_add = regex_result.groups()
                if raw_root_path is None:
                    root_path = ''
                else:
                    root_path = raw_root_path
                # Searching in the database
                key = root_path + '/' + key_to_add
                key_to_binary = self.utils.encode_str_to_byte(key)
                value = self.db_values.get_value(key_to_binary)
                # If not, we will try to create the entry process.
                if value is None:
                    volume = self.pick_a_volume()
                    if volume is None:
                        self.messenger.code_type = self.const.PULZAR_ERROR
                        self.messenger.mark_as_failed()
                        self.messenger.set_message = 'Not volumes sync'
                        return self.messenger
                    # Populating dictionary with the info needed.
                    self.messenger.code_type = self.const.REDIRECT_PUT
                    self.messenger.http_code = '307 temporary redirect'
                    self.messenger.volume = volume
                    return self.messenger
                # Since key was found, an element was already added before
                # using the same key.
                self.messenger.code_type = self.const.KEY_ALREADY_ADDED

            except Exception as err:
                print('Error PUT process:', err)
                self.messenger.code_type = self.const.PULZAR_ERROR
                self.messenger.mark_as_failed()
                self.messenger.set_message = str(err)

        else:
            self.messenger.code_type = self.const.USER_ERROR
            self.messenger.mark_as_failed()
            self.messenger.set_message = 'Wrong query'

        return self.messenger
