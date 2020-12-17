import importlib
from pulzarutils.utils import Utils
from pulzarutils.constants import ReqType
from pulzarutils.messenger import Messenger
from pulzarutils.stream import Config
from pulzarcore.core_request import CoreRequest
from pulzarcore.core_db import DB
from pulzarcore.core_job_node import Job
from pulzarcore.core_body import Body


class JobProcess:
    """Main class to handle jobs
    """

    def __init__(self, constants):
        self.TAG = self.__class__.__name__
        self.const = constants
        self.utils = Utils()
        self.db_backup = DB(self.const.DB_BACKUP)
        self.config = Config(self.const.CONF_PATH)
        self.messenger = Messenger()

    def process_request(self, url_path, env):
        """Receiving the order to launch a job
        """
        try:
            # Extracting data
            body = Body()
            params = body.extract_params(env)
            if self.const.DEBUG:
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
                print('First you need to set/create the job directory')
                self.messenger.code_type = self.const.JOB_ERROR
                self.messenger.set_message = 'first you need to set/create the job directory'
                self.messenger.mark_as_failed()
                return self.messenger
            # check if the job exists
            path_to_search = self.job_directory + job_file_path + '/' + job_file_name + '.py'
            generic_path = job_file_path + '/' + job_file_name + '.py'
            if self.const.DEBUG:
                print('path: ', path_to_search)
            good = False
            if self.utils.file_exists(path_to_search):
                job_object = Job(job_id, generic_path,
                                 job_parameters, job_scheduled)
                good = job_object.schedule_job(self.const)

            # Response
            if good:
                self.messenger.code_type = self.const.JOB_OK
                self.messenger.set_message = 'ok'
            else:
                self.messenger.code_type = self.const.JOB_ERROR
                self.messenger.set_message = 'job does not exist'
                self.messenger.mark_as_failed()

        except Exception as err:
            print('ERROR::{}::{}'.format(self.TAG, err))
            self.messenger.code_type = self.const.PULZAR_ERROR
            self.messenger.set_message = str(err)
            self.messenger.mark_as_failed()

        return self.messenger
