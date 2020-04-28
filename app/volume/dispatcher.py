from utils.constants import Constants
from volume.get_process import GetProcess
from volume.post_process import PostProcess
from volume.delete_process import DeleteProcess


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

        # Response to master, can or not contains data as parameter
        self.complex_response = {
            'action': None,
            'parameters': None
        }

    def classify_request(self, env, start_response):
        """Return the type
        """
        url_path = env[self.const.PATH_INFO]
        method = env[self.const.REQUEST_METHOD]
        
        # Admin
        if self.utils.match_regex(url_path, self.re_skynet):
            return self.const.ADMIN

        # General requests
        else:
            # Delete value.
            if method == self.const.DELETE:
                get_request = DeleteProcess(self.const)
                response = get_request.process_request(
                    env, start_response, url_path)

                self.complex_response = response
            # Get key-value.
            if method == self.const.GET:
                get_request = GetProcess(self.const)
                response = get_request.process_request(
                    env, start_response, url_path)

                self.complex_response = response
                return self.complex_response

            # Post key-value.
            if method == self.const.POST:
                post_request = PostProcess(self.const)
                self.complex_response = post_request.process_request(
                    env, start_response, url_path)
        return self.complex_response
