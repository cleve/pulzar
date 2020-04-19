from utils.constants import Constants
from utils.utils import Utils
from core.core_request import CoreRequest
from volume.dispatcher import Dispatcher
from core.core_db import DB


class Volume:
    def __init__(self):
        self.const = Constants()
        self.utils = Utils()
        self.dispatcher = Dispatcher(self.utils)
        self.volume_env = None
        self.master_url = None
        self.master_port = None

    def save_status(self):
        """Save stats to synch
        """
        db = DB(self.const.DB_STATS)
        db.update_or_insert_value(
            self.utils.encode_str_to_byte(self.const.SERVER_NAME),
            self.utils.encode_str_to_byte(
                self.volume_env[self.const.SERVER_NAME])
        )
        db.update_or_insert_value(
            self.utils.encode_str_to_byte(self.const.SERVER_PORT),
            self.utils.encode_str_to_byte(
                self.volume_env[self.const.SERVER_PORT])
        )

    def process_request(self, env, start_response):
        # Get request type
        self.volume_env = self.utils.extract_host_env(env)
        self.save_status()
        request = self.dispatcher.classify_request(env, start_response)
        request_type = request['action']
        if request_type == self.const.NOTIFY_KEY_TO_MASTER:
            # Report the register creation.
            master_url = self.utils.extract_url_data(
                self.volume_env['QUERY_STRING'])

        return request_type
