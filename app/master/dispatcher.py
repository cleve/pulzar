from utils.constants import Constants
from master.skynet import Skynet
from master.get_process import GetProcess

class Dispatcher:
    """Calssify the type of request:
     - regular
     - admin
     - skynet
     """
    def __init__(self, utils):
        self.utils = utils
        self.const = Constants()
        
        # reg strings
        self.re_admin = r'/admin/\w'
        self.re_skynet = r'/skynet/\w'

    def classify_request(self, essential_env, env, start_response):
        """Return the type
        """
        url_path = essential_env[self.const.PATH_INFO]
        method = essential_env[self.const.REQUEST_METHOD]
        # Skynet
        if self.utils.match_regex(url_path, self.re_skynet):
            skynet = Skynet(env)
            skynet.process_request(url_path, method)    
            return self.const.SKYNET

        # Admin
        elif self.utils.match_regex(url_path, self.re_skynet):
            return self.const.ADMIN

        # General requests
        else:
            # Get value or store values
            if essential_env[self.const.REQUEST_METHOD] == self.const.GET:
                get_request = GetProcess(self.const)
                get_request.process_request(env, start_response, url_path)
                return self.const.REGULAR_GET

    

