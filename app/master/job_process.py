from utils.utils import Utils
from utils.constants import ReqType
from utils.node_utils import NodeUtils
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

    def notify_record_to_master(self, env):

        # Report the register creation.
        master_url = self.utils.extract_url_data(
            env['QUERY_STRING'])
        # Confirming with master.
        req = CoreRequest(
            master_url['host'], master_url['port'], self.const.ADD_RECORD)
        req.set_type(ReqType.POST)
        req.set_path(self.const.ADD_RECORD)
        # We have to send the key, volume and port.
        req.set_payload({
            'key': 'self.file_utils.key',
            'volume': env[self.const.HTTP_HOST]
        })
        if not req.make_request():
            # If an error ocurr in the server, we need to delete the file.

            return False

        return True

    def process_request(self, url_path, query_string, env):
        """Processing job request
        """
        try:
            job_path = self.utils.get_search_regex(
                url_path,
                self.const.RE_LAUNCH_JOB
            )
            # parameters to send to a node
            params = {}
            job_path, job_name = job_path.groups()
            body = Body()
            job_params = body.extract_params(env)
            params['job_path'] = job_path
            params['job_name'] = job_name
            params['job_id'] = None
            params['parameters'] = job_params
            print('params:', params)

            job_object = Job(params)
            if job_object.send_job(self.const):
                self.complex_response['action'] = self.const.JOB_RESPONSE
            self.complex_response['action'] = self.const.JOB_ERROR

        except Exception as err:
            print('Error extracting keywerwe', err)
            self.complex_response['action'] = self.const.JOB_ERROR

        return self.complex_response
