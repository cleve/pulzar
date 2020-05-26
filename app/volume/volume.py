from utils.constants import Constants
from utils.constants import ReqType
from utils.utils import Utils
from utils.file_utils import FileUtils
from core.core_request import CoreRequest
from volume.dispatcher import Dispatcher
from core.core_db import DB
from core.core_response import ResponseClass


class Volume:
    def __init__(self):
        self.const = Constants()
        self.utils = Utils()
        self.file_utils = FileUtils(self.const)
        self.response = ResponseClass()
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
        db.update_or_insert_value(
            self.utils.encode_str_to_byte('restored'),
            self.utils.encode_str_to_byte('ready')
        )

    def process_request(self, env, start_response):
        # Get request type
        self.volume_env = self.utils.extract_host_env(env)
        self.save_status()
        request = self.dispatcher.classify_request(env, start_response)
        request_type = request['action']
        if request_type == self.const.AUTODISCOVERY:
            self.response.set_response('200 OK')
            self.response.set_message(b'discovered')
        if request_type == self.const.KEY_DELETED:
            self.response.set_response('200 Deleted')
            self.response.set_message(b'record deleted')
        if request_type == self.const.KEY_ADDED:
            self.response.set_response('201 Created')
            self.response.set_message(b'record added')
        if request_type == self.const.KEY_ERROR:
            self.response.set_response('406 Not acceptable')
            self.response.set_message(b'record already added')
        if request_type == self.const.KEY_NOT_FOUND:
            self.response.set_response('404 Not found')
            self.response.set_message(b'key not found')
        if request_type == self.const.KEY_FOUND:
            return self.file_utils.read_value(request['parameters'], start_response)
        return self.response.get_response(start_response)
