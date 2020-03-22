from utils.constants import Constants
from master.skynet import Skynet

class Dispatcher:
    """Calssify the type of request:
     - regular
     - admin
     - skynet
     """
    def __init__(self, utils):
        self.utils = utils
        self.const = Constants()
        self.skynet = Skynet()

        # reg strings
        self.re_regular = r''
        self.re_admin = r'/admin/\w'
        self.re_skynet = r'/skynet/\w'

    def classify_request(self, env):
        """Return the type
        """
        url_path = env[self.const.PATH_INFO]
        # Skynet
        if self.utils.match_regex(url_path, self.re_skynet):
            pass

        # Admin
        elif self.utils.match_regex(url_path, self.re_skynet):
            pass

        # General requests
        else:
            pass

    

