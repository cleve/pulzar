from pulzarutils.constants import Constants
from pulzarutils.messenger import Messenger
from pulzarutils.logger import PulzarLogger
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

    def __init__(self, utils):
        self.utils = utils
        self.const = Constants()
        self.logger = PulzarLogger(self.const)

        # reg strings
        self.re_admin = r'/admin/\w'
        self.re_skynet = r'/skynet/\w'
        self.re_job = r'/send_job$'
        self.re_autodiscovery = r'/autodiscovery$'

    def classify_request(self, env, start_response):
        """Return the type
        """
        url_path = env[self.const.PATH_INFO]
        method = env[self.const.REQUEST_METHOD]

        # Autodiscovery
        if self.utils.match_regex(url_path, self.re_autodiscovery):
            discovery_process = DiscoveryProcess(self.const, self.logger)
            return discovery_process.process_request(env)

        # Admin
        if self.utils.match_regex(url_path, self.re_admin):
            admin_process = AdminProcess(self.const, self.logger)
            if method == self.const.GET:
                return admin_process.process_request(url_path)

        # Jobs
        if self.utils.match_regex(url_path, self.re_job):
            if method == self.const.POST:
                job_process = JobProcess(self.const, self.logger)
                return job_process.process_request(url_path, env)

        # Regular requests
        else:
            # Delete value.
            if method == self.const.DELETE:
                get_request = DeleteProcess(self.const, self.logger)
                return get_request.process_request(
                    env, start_response, url_path)

            # Get key-value.
            if method == self.const.GET:
                get_request = GetProcess(self.const, self.logger)
                return get_request.process_request(
                    env, start_response, url_path)

            # PUT key-value.
            if method == self.const.PUT:
                put_request = PutProcess(self.const, self.logger)
                return put_request.process_request(
                    env, start_response, url_path)

        # Generic response
        messenger = Messenger()
        messenger.code_type = self.const.PULZAR_ERROR
        messenger.set_message = 'internal error'
        return messenger
