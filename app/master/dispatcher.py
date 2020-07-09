from utils.constants import Constants
from master.skynet import Skynet
from master.get_process import GetProcess
from master.post_process import PostProcess
from master.put_process import PutProcess
from master.delete_process import DeleteProcess
from master.third_party_process import TPProcess
from master.admin_process import AdminProcess


class Dispatcher:
    """Calssify the type of request:
     - regular[GET/POST]
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

    def classify_request(self, essential_env, env, start_response):
        """Return dictionary complex_response {action, parameters}
        """
        url_path = essential_env[self.const.PATH_INFO]
        method = essential_env[self.const.REQUEST_METHOD]
        # Skynet
        if self.utils.match_regex(url_path, self.re_skynet):
            skynet = Skynet(env)
            action, synch_complete = skynet.process_request(
                url_path, method)
            self.complex_response['action'] = action
            self.complex_response['parameters'] = synch_complete
            return self.complex_response

        # Admin
        elif self.utils.match_regex(url_path, self.re_admin):
            if method == self.const.GET:
                admin_process = AdminProcess(self.const)
                self.complex_response = admin_process.process_request(url_path)
                return self.complex_response

        # Third party
        elif self.utils.match_regex(url_path, self.const.RE_THIRD_PARTY):
            if method == self.const.GET:
                third_party = TPProcess(self.const)
                self.complex_response = third_party.process_request(url_path)

        # General requests
        else:
            # Delete value.
            if method == self.const.DELETE:
                delete_request = DeleteProcess(self.const)
                self.complex_response = delete_request.process_request(
                    env, start_response, url_path)

            # Get key-value.
            if method == self.const.GET:
                get_request = GetProcess(self.const)
                self.complex_response = get_request.process_request(
                    env, start_response, url_path)

                return self.complex_response

            # Post key-value.
            if method == self.const.POST:
                post_request = PostProcess(self.const)
                self.complex_response = post_request.process_request(
                    env, start_response, url_path)

            # Put key-value.
            if method == self.const.PUT:
                put_request = PutProcess(self.const)
                self.complex_response = put_request.process_request(
                    env, start_response, url_path)
        return self.complex_response
