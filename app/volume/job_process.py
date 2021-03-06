from pulzarutils.utils import Utils
from pulzarutils.utils import Constants
from pulzarutils.messenger import Messenger
from pulzarutils.stream import Config
from pulzarcore.core_request import CoreRequest
from pulzarcore.core_db import DB
from pulzarcore.core_job_node import Job
from pulzarcore.core_body import Body


class JobProcess:
    """Main class to handle jobs
    """

    def __init__(self, logger):
        self.TAG = self.__class__.__name__
        self.logger = logger
        self.utils = Utils()
        self.db_backup = DB(Constants.DB_BACKUP)
        self.config = Config(Constants.CONF_PATH)
        self.messenger = Messenger()

    def process_request(self, url_path, env):
        """Receiving the order to launch a job
        """
        try:
            # Checking the passport
            if not self.utils.check_passport(env):
                self.messenger.code_type = Constants.JOB_ERROR
                self.messenger.set_message = 'invalid passport, contact to the admin'
                self.messenger.mark_as_failed()
                return self.messenger
            # Extracting data
            body = Body()
            params = body.extract_params(env)
            if Constants.DEBUG:
                print('params for job', params)

            # Scheduling job
            job_id = params['job_id']
            job_file_name = params['job_name']
            job_file_path = params['job_path']
            job_parameters = params['parameters']
            job_scheduled = params['scheduled']

            # Get job path directory
            self.job_directory = self.config.get_config('jobs', 'dir')
            if self.job_directory is None:
                self.logger.debug(':{}:path -> {}'.format(self.TAG, 'First you need to set/create the job directory'))
                self.messenger.code_type = Constants.JOB_ERROR
                self.messenger.set_message = 'first you need to set/create the job directory'
                self.messenger.mark_as_failed()
                return self.messenger
            # check if the job exists
            path_to_search = self.job_directory + job_file_path + '/' + job_file_name + '.py'
            generic_path = job_file_path + '/' + job_file_name + '.py'
            self.logger.debug(':{}:path -> {}'.format(self.TAG, path_to_search))
            good = False
            if self.utils.file_exists(path_to_search):
                job_object = Job(job_id, generic_path,
                                 job_parameters, job_scheduled)
                good = job_object.schedule_job()

            # Response
            if good:
                self.messenger.code_type = Constants.JOB_OK
                self.messenger.set_message = 'ok'
            else:
                self.messenger.code_type = Constants.JOB_ERROR
                self.messenger.set_message = 'job does not exist'
                self.messenger.mark_as_failed()

        except Exception as err:
            self.logger.exception(':{}:{}'.format(self.TAG, err))
            self.messenger.code_type = Constants.PULZAR_ERROR
            self.messenger.set_message = str(err)
            self.messenger.mark_as_failed()

        return self.messenger
