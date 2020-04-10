from utils.constants import Constants
from utils.utils import Utils
from master.dispatcher import Dispatcher


class Master:
    def __init__(self):
        self.const = Constants()
        self.utils = Utils()
        self.dispatcher = Dispatcher(self.utils)
        self.master_env = None

    def process_request(self, env, start_response):
        # Get request type
        self.essential_env = self.utils.extract_host_env(env)
        request = self.dispatcher.classify_request(
            self.essential_env, env, start_response)
        request_type = request['action']
        print(request)
        # If not Skynet or administrative tasks
        if request_type == self.const.REGULAR_GET:
            # Here redirection or negotiation
            pass
        return request_type
