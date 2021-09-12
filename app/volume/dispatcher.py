from pulzarutils.constants import Constants
from pulzarutils.messenger import Messenger
from volume.get_process import GetProcess
from volume.discovery_process import DiscoveryProcess
from volume.put_process import PutProcess
from volume.delete_process import DeleteProcess
from volume.admin_process import AdminProcess
from volume.job_process import JobProcess


class Dispatcher:
    """Classify the type of request:
     - regular
     - admin
     - skynet
     """

    def __init__(self, utils, logger):
        self.utils = utils
        self.logger = logger

        # reg strings
        self.re_admin = r'/admin/\w'
        self.re_skynet = r'/skynet/\w'
        self.re_job = r'/send_job$'
        self.re_autodiscovery = r'/autodiscovery$'

    def classify_request(self, env, start_response):
        """Return the type
        """
        url_path = env[Constants.PATH_INFO]
        method = env[Constants.REQUEST_METHOD]

        # Autodiscovery
        if self.utils.match_regex(url_path, self.re_autodiscovery):
            discovery_process = DiscoveryProcess(self.logger)
            return discovery_process.process_request(env)

        # Admin
        if self.utils.match_regex(url_path, self.re_admin):
            admin_process = AdminProcess(self.logger)
            if method == Constants.GET:
                return admin_process.process_request(url_path)

        # Regular requests
        else:
            # Delete value.
            if method == Constants.DELETE:
                get_request = DeleteProcess(self.logger)
                return get_request.process_request(
                    env, start_response, url_path)

            # Get key-value.
            if method == Constants.GET:
                get_request = GetProcess(self.logger)
                return get_request.process_request(
                    env, start_response, url_path)

            # PUT key-value.
            if method == Constants.PUT:
                put_request = PutProcess(self.logger)
                return put_request.process_request(
                    env, start_response, url_path)

        # Generic response
        messenger = Messenger()
        messenger.code_type = Constants.PULZAR_ERROR
        messenger.set_message = 'internal error'
        return messenger
