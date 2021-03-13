from pulzarutils.utils import Utils
from pulzarutils.utils import Constants
from pulzarutils.stream import Config
from pulzarutils.messenger import Messenger
from pulzarcore.core_db import DB


class PutProcess:
    def __init__(self, logger):
        self.TAG = self.__class__.__name__
        self.logger = logger
        # 20 mins max to consider a volume online.
        self.second_range = 1200
        self.utils = Utils()
        # DB of values already loaded.
        self.db_values = DB(Constants.DB_PATH)
        # DB of volumes/keys.
        self.db_volumes = DB(Constants.DB_VOLUME)
        self.messenger = Messenger()

    def pick_a_volume(self, env):
        config = Config(Constants.CONF_PATH)
        # First checking the size allowed.
        try:
            request_body_size = int(env[Constants.CONTENT_LENGTH])
        except (ValueError):
            request_body_size = 0
        max_size = int(config.get_config('general', 'maxsize'))
        to_mb = self.utils.bytesto(request_body_size, 'm')
        if to_mb > max_size:
            raise Exception(
                'max size allowed is {}MB'.format(max_size))
        # Selecting port
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
            url_path, Constants.RE_PUT_VALUE)

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
                    volume = self.pick_a_volume(env)
                    if volume is None:
                        self.messenger.code_type = Constants.PULZAR_ERROR
                        self.messenger.mark_as_failed()
                        self.messenger.set_message = 'Not volumes sync'
                        return self.messenger
                    # Populating dictionary with the info needed.
                    self.messenger.code_type = Constants.REDIRECT_PUT
                    self.messenger.http_code = '307 temporary redirect'
                    self.messenger.volume = volume
                    return self.messenger
                # Since key was found, an element was already added before
                # using the same key.
                self.messenger.code_type = Constants.KEY_ALREADY_ADDED

            except Exception as err:
                self.logger.exception('{}:{}'.format(self.TAG, err))
                self.messenger.code_type = Constants.PULZAR_ERROR
                self.messenger.mark_as_failed()
                self.messenger.set_message = str(err)

        else:
            self.messenger.code_type = Constants.USER_ERROR
            self.messenger.mark_as_failed()
            self.messenger.set_message = 'Wrong query'

        return self.messenger
