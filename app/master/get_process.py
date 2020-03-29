from utils.utils import Utils

class GetProcess:
    def __init__(self, constants):
        self.const = constants
        self.utils = Utils()

    def process_request(self, env, start_response, url_path):
        # Get request type
        print('path', url_path)