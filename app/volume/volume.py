from utils.constants import Constants
from utils.utils import Utils
from core.core_request import CoreRequest
from volume.dispatcher import Dispatcher

class Volume:
    def __init__(self):
        self.const = Constants()
        self.utils = Utils()
        self.dispatcher = Dispatcher(self.utils)
        self.volume_env = None
        self.master_url = None
        self.master_port = None

    def send_status(self):
        """After the cycle, send stats to the server
        """
        # Gets disk usage
        percent = self.utils.giga_free_space()
        url_path = self.const.SYNC + '/' + self.volume_env[self.const.SERVER_NAME] + '/' + percent 
        if self.master_url is not None and self.master_port is not None:
            req = CoreRequest(
                self.master_url,
                self.master_port,
                url_path
            )

            if req.make_request():
                print('synchronized')
    
    def process_request(self, env, start_response):
        # Get request type
        self.volume_env = self.utils.extract_host_env(env)
        request_type = self.dispatcher.classify_request(env)
        return request_type


