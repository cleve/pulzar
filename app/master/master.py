from utils.constants import Constants
from utils.utils import Utils
from master.dispatcher import Dispatcher

class Master:
    def __init__(self):
        self.const = Constants()
        self.utils = Utils()
        self.dispatcher = Dispatcher(self.utils)
        self.volume_env = None

    def process_request(self, env, start_response):
        # Get request type
        self.volume_env = self.utils.extract_host_env(env)
        request_type = self.dispatcher.classify_request(env)
        return request_type


