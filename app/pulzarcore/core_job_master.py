from pulzarcore.core_request import CoreRequest
from pulzarcore.core_rdb import RDB
from pulzarutils.node_utils import NodeUtils
from pulzarutils.constants import ReqType
from pulzarutils.utils import Utils


class Job:
    """Send tasks to the nodes
    """

    def __init__(self, job_params):
        self.job_params = job_params
        self.utils = Utils()
        self.job_id = None

    def unregister_job(self, path_db_jobs):
        """Mark as failed job in master
        """
        print('uregistering job')
        # Master job database
        data_base = RDB(path_db_jobs)
        sql = 'UPDATE job SET state = 2 WHERE id = {}'.format(self.job_id)
        data_base.execute_sql(
            sql
        )

    def register_job(self, path_db_jobs, node):
        """Register job in master
        """
        print('registering job')
        job_path = self.job_params['job_path']
        job_name = self.job_params['job_name']
        parameters = self.utils.py_to_json(self.job_params['parameters'])
        # Master job database
        data_base = RDB(path_db_jobs)
        sql = 'INSERT INTO job (job_name, job_path, parameters, node, creation_time, state) values (?, ?, ?, ?, ?, ?)'
        self.job_id = data_base.execute_sql_insert(
            sql,
            (
                job_name, job_path, parameters, node, self.utils.get_current_datetime(), 0
            )
        )

    def send_job(self, const):
        """Send job to the node selected

            params:
             - const (Constants)
        """

        node_utils = NodeUtils(const)
        node = node_utils.pick_a_volume()
        if node is None:
            return False
        print('Sending job to node ', node)
        # Register in data base
        self.register_job(const.DB_JOBS, node.decode())
        if self.job_id is None:
            return False
        self.job_params['job_id'] = self.job_id
        request = CoreRequest(node.decode(), '9001', '/send_job')
        request.set_type(ReqType.POST)
        request.set_payload(self.job_params)
        job_response = request.make_request(json_request=True)
        if not job_response:
            # removing job
            self.unregister_job(const.DB_JOBS)
        return job_response
