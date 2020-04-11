from utils.utils import Utils
from core.core_db import DB


class PostProcess:
    def __init__(self, constants):
        self.const = constants
        self.utils = Utils()
        # DB of values already loaded.
        self.db_values = DB(self.const.DB_PATH)
        # DB of volumes/keys.
        self.db_volumes = DB(self.const.DB_VOLUME)
        # DB of volume stats reported.
        self.db_volumes_st = DB(self.const.DB_STATS)

    def pick_a_volume(self):
        volumes = self.db_volumes.get_keys_values()
        print(volumes)
        min_value = 100
        server = None
        for elem in volumes:
            print('elem', elem)
            percent = int(self.utils.decode_byte_to_str(elem[1]))
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
                if value is None:
                    print('key_to_binary >>', key_to_binary)
                    volume = self.pick_a_volume()
                    print('server ::: ', volume)
                    return self.const.KEY_NOT_FOUND

            except Exception as err:
                print('Error extracting key', err)
