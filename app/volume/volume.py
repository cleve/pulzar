from pulzarutils.constants import Constants
from pulzarutils.constants import ReqType
from pulzarutils.utils import Utils
from pulzarutils.logger import PulzarLogger
from pulzarutils.file_utils import FileUtils
from pulzarcore.core_request import CoreRequest
from volume.dispatcher import Dispatcher
from pulzarcore.core_db import DB
from pulzarcore.core_response import ResponseClass


class Volume:
    def __init__(self):
        self.const = Constants()
        self.utils = Utils()
        self.file_utils = FileUtils(self.const)
        self.response = ResponseClass()
        self.logger = PulzarLogger(self.const, master=False)
        self.dispatcher = Dispatcher(self.utils, self.logger)
        self.master_url = None
        self.master_port = None

    def process_request(self, env, start_response):
        # Get request type
        message = self.dispatcher.classify_request(env, start_response)
        request_type = message.code_type
        # First the general errors
        if request_type == self.const.PULZAR_ERROR or request_type == self.const.USER_ERROR:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())
        if request_type == self.const.BACKUP_SCHEDULED:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())
        elif request_type == self.const.AUTODISCOVERY:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())
        elif request_type == self.const.KEY_DELETED:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())
        elif request_type == self.const.KEY_ADDED:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())
        elif request_type == self.const.KEY_ERROR:
            self.response.set_response('406 Not acceptable')
            self.response.set_message(b'record already added')
        elif request_type == self.const.KEY_NOT_FOUND:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())
        elif request_type == self.const.KEY_FOUND:
            return self.file_utils.read_value(message.extra, start_response)
        elif request_type == self.const.JOB_OK:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())
        else:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())
        return self.response.get_response(start_response)
