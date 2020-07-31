import importlib
from utils.utils import Utils
from utils.constants import ReqType
from core.core_request import CoreRequest
from core.core_db import DB
from core.core_job import Job
from core.core_body import Body


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
            job_file_name = params['job_name']
            job_file_path = params['job_path']
            job_parameters = params['parameters']

            # check if the job exists
            path_to_search = 'jobs' + job_file_path + '/' + job_file_name + '.py'
            print('path: ', path_to_search)
            if self.utils.file_exists(path_to_search):
                print('Job exists, scheduling ', job_file_name)

            # Response
            if True:
                print('======')
                self.complex_response['action'] = self.const.JOB_OK
            else:
                self.complex_response['action'] = self.const.KEY_ERROR

        except Exception as err:
            print('Error extracting key', err)
            self.complex_response['action'] = self.const.KEY_ERROR

        return self.complex_response
