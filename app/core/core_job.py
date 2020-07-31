# Internal imports
from core.core_request import CoreRequest
from utils.node_utils import NodeUtils
from utils.constants import ReqType
from utils.utils import Utils
from core.core_rdb import RDB


class Job:
    """Send tasks to the nodes
    """

    def __init__(self, job_params):
        self.job_params = job_params
        self.utils = Utils()

    def register_job(self, path_db_jobs):
        """Register job in master
        """
        print('registering job')
        job_path = self.job_params['job_path'] + self.job_params['job_name']
        parameters = self.utils.py_to_json(self.job_params['parameters'])
        # Master job database
        data_base = RDB(path_db_jobs)
        sql = 'INSERT INTO job (job_name, parameters, creation_time, ready) values (?, ?, ?, ?)'
        data_base.execute_sql_with_params(
            sql,
            (
                job_path, parameters, self.utils.get_current_datetime(), 0
            )
        )

    def send_job(self, const):
        """Send job to the node selected

            params:
             - const (Constants)
        """

        node_utils = NodeUtils(const)
        node = node_utils.pick_a_volume()
        print('Sending job')
        request = CoreRequest(node.decode(), '9001', '/send_job')
        request.set_type(ReqType.POST)
        request.set_payload(self.job_params)
        job_response = request.make_request(json_request=True)
        if job_response:
            # Register in data base
            self.register_job(const.DB_JOBS)
        return job_response
