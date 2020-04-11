from utils.constants import Constants
from utils.utils import Utils
from master.dispatcher import Dispatcher
from core.core_response import ResponseClass


class Master:
    def __init__(self):
        self.const = Constants()
        self.utils = Utils()
        self.dispatcher = Dispatcher(self.utils)
        self.response = ResponseClass()
        self.master_env = None

    def process_request(self, env, start_response):
        # Get request type
        self.essential_env = self.utils.extract_host_env(env)
        request = self.dispatcher.classify_request(
            self.essential_env, env, start_response)
        request_type = request['action']
        print(request)
        if request_type == self.const.SKYNET:
            self.response.set_response('200 OK')
            self.response.set_message(b'synch ok')

        # If not Skynet or administrative tasks
        if request_type == self.const.KEY_NOT_FOUND:
            self.response.set_response('200 OK')
            self.response.set_message(b'key not found')

        if request_type == self.const.REGULAR_GET:
            # Here redirection or negotiation
            print('GET REGULAR')

        if request_type == self.const.REDIRECT_POST:
            self.response.set_response('302 permanent redirect')
            self.response.set_redirection('http://google.com')
            self.response.set_message(b'ok')

        return self.response.get_response(start_response)
