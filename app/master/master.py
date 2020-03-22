from utils.constants import Constants
from utils.utils import Utils
from master.dispatcher import Dispatcher

class Master:
    def __init__(self):
        self.const = Constants()
        self.utils = Utils()
        self.dispatcher = Dispatcher(self.utils)

    def process_request(self, env, start_response):
        # Get request type
        request_type = self.dispatcher.classify_request(env)


