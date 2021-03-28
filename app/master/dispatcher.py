from pulzarutils.constants import Constants
from pulzarutils.messenger import Messenger
from .skynet import Skynet
from .get_process import GetProcess
from .job_process import JobProcess
from .put_process import PutProcess
from .get_node_process import GetNodeProcess
from .delete_process import DeleteProcess
from .extension_process import ExtensionProcess
from .admin_process import AdminProcess
from .admin_jobs import AdminJobs


class Dispatcher:
    """Calssify the type of request:
     - regular[GET/POST]
     - admin
     - skynet
     """

    def __init__(self, utils, logger):
        self.utils = utils
        self.logger = logger

        # reg strings
        self.re_job_admin = r'\/admin\/(scheduled_jobs|jobs|all_jobs|job_catalog){1}.*'
        self.re_admin = r'\/admin\/\w'
        self.re_skynet = r'\/skynet\/\w'

    def classify_request(self, essential_env, env, start_response):
        """Return dictionary complex_response {action, parameters}
        """
        url_path = essential_env[Constants.PATH_INFO]
        method = essential_env[Constants.REQUEST_METHOD]
        # OPTION method
        if method == 'OPTIONS':
            messenger = Messenger()
            messenger.code_type = Constants.OPTIONS
            messenger.set_message = 'options'
            return messenger
        # Skynet
        if self.utils.match_regex(url_path, self.re_skynet):
            skynet = Skynet(env, self.logger)
            return skynet.process_request(url_path, method)

        # Job Admin
        elif self.utils.match_regex(url_path, self.re_job_admin):
            if method == Constants.GET:
                query_string = env['QUERY_STRING']
                admin_process = AdminJobs(self.logger)
                if query_string.strip() != '':
                    url_path += '?' + query_string
                return admin_process.process_request(url_path)
            else:
                messenger = Messenger()
                messenger.code_type = Constants.USER_ERROR
                messenger.mark_as_failed()
                messenger.set_message = 'Method used does not match, try GET'
                return messenger

        # Admin
        elif self.utils.match_regex(url_path, self.re_admin):
            if method == Constants.GET:
                admin_process = AdminProcess(self.logger)
                return admin_process.process_request(url_path)
            else:
                messenger = Messenger()
                messenger.code_type = Constants.USER_ERROR
                messenger.mark_as_failed()
                messenger.set_message = 'Method used does not match'
                return messenger

        # Jobs
        elif self.utils.match_regex(url_path, Constants.RE_LAUNCH_JOB) or self.utils.match_regex(url_path, Constants.RE_CANCEL_JOB):
            if method == Constants.POST:
                job_process = JobProcess(self.logger)
                query_string = env['QUERY_STRING']
                return job_process.process_request(
                    url_path, query_string, env)
            else:
                messenger = Messenger()
                messenger.code_type = Constants.USER_ERROR
                messenger.mark_as_failed()
                messenger.set_message = 'Method used does not match, try with POST'
                return messenger

        elif self.utils.match_regex(url_path, Constants.RE_NOTIFICATION_JOB):
            if method == Constants.POST:
                job_process = JobProcess(self.logger)
                query_string = env['QUERY_STRING']
                return job_process.process_notification_request(
                    url_path, query_string, env)
            else:
                messenger = Messenger()
                messenger.code_type = Constants.USER_ERROR
                messenger.mark_as_failed()
                messenger.set_message = 'Method used does not match'
                return messenger

        # Extensions
        elif self.utils.match_regex(url_path, Constants.RE_EXTENSION):
            if method == Constants.GET:
                extension = ExtensionProcess(self.logger)
                query_string = env['QUERY_STRING']
                return extension.process_request(
                    url_path, query_string)

            elif method == Constants.PUT:
                extension = ExtensionProcess(self.logger)
                query_string = env['QUERY_STRING']
                return extension.process_request(
                    url_path, query_string, env)

            else:
                messenger = Messenger()
                messenger.code_type = Constants.USER_ERROR
                messenger.mark_as_failed()
                messenger.set_message = 'Method used does not match'
                return messenger

        # Request storage
        elif self.utils.match_regex(url_path, Constants.RE_GET_STORAGE):
            if method == Constants.GET:
                get_node_request = GetNodeProcess(self.logger)
                return get_node_request.process_request(
                    env, start_response, url_path)

        # General requests
        else:
            # Delete value.
            if method == Constants.DELETE:
                delete_request = DeleteProcess(self.logger)
                return delete_request.process_request(
                    env, start_response, url_path)

            # Get key-value.
            if method == Constants.GET:
                get_request = GetProcess(self.logger)
                return get_request.process_request(
                    env, start_response, url_path)

            # Put key-value.
            if method == Constants.PUT:
                put_request = PutProcess(self.logger)
                return put_request.process_request(
                    env, start_response, url_path)

            else:
                return Messenger()
        return Messenger()
