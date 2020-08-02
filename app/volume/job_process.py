import importlib
from pulzarutils.utils import Utils
from pulzarutils.constants import ReqType
from pulzarcore.core_request import CoreRequest
from pulzarcore.core_db import DB
from pulzarcore.core_job_node import Job
from pulzarcore.core_body import Body


class JobProcess:
    """Main class to handle jobs
    """

    def __init__(self, constants):
        self.const = constants
        self.utils = Utils()
        self.db_backup = DB(self.const.DB_BACKUP)
        self.complex_response = {
            'action': None,
            'parameters': None,
            'volume': None
        }

    def process_request(self, url_path, env):
        """Receiving the order to launch a job
        """
        try:
            # Extracting data
            body = Body()
            params = body.extract_params(env)
            print('params for job', params)

            # Scheduling job
            job_id = params['job_id']
            job_file_name = params['job_name']
            job_file_path = params['job_path']
            job_parameters = params['parameters']

            # check if the job exists
            path_to_search = 'jobs' + job_file_path + '/' + job_file_name + '.py'
            print('path: ', path_to_search)
            good = False
            if self.utils.file_exists(path_to_search):
                print('Job exists, scheduling ', job_file_name)
                job_object = Job(job_id, path_to_search, job_parameters)
                good = job_object.schedule_job(self.const)

            # Response
            if good:
                self.complex_response['action'] = self.const.JOB_OK
            else:
                self.complex_response['action'] = self.const.KEY_ERROR

        except Exception as err:
            print('Error extracting key', err)
            self.complex_response['action'] = self.const.KEY_ERROR

        return self.complex_response
