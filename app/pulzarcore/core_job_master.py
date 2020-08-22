from pulzarcore.core_request import CoreRequest
from pulzarcore.core_rdb import RDB
from pulzarcore.core_db import DB
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
        self.scheduler_options = [
            'minutes',
            'hours',
            'days',
            'weeks'
        ]

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

    def register_scheduled_job(self, path_db_jobs):
        """Register schedule job in master
        """
        print('registering scheduled job')
        job_path = self.job_params['job_path']
        job_name = self.job_params['job_name']

        # Scheduler
        scheduler_object = self.job_params['parameters']['scheduled']

        # Checking scheduler options
        if scheduler_object['interval'] not in self.scheduler_options:
            return False

        # Removing extra params
        del self.job_params['parameters']['scheduled']
        parameters = self.utils.py_to_json(self.job_params['parameters'])
        # Master job database
        data_base = RDB(path_db_jobs)
        sql = 'INSERT INTO schedule_job (job_name, job_path, parameters, interval, time_unit, repeat, state) values (?, ?, ?, ?, ?, ?, ?)'
        self.job_id = data_base.execute_sql_insert(
            sql,
            (
                job_name,
                job_path,
                parameters,
                scheduler_object['interval'],
                scheduler_object['time_unit'],
                scheduler_object['repeat'],
                0
            )
        )

        return True

    def register_job(self, path_db_jobs, node):
        """Register job in master
        """
        print('registering job')
        job_path = self.job_params['job_path']
        job_name = self.job_params['job_name']
        parameters = self.utils.py_to_json(self.job_params['parameters'])
        # Master job database
        data_base = RDB(path_db_jobs)
        sql = 'INSERT INTO job (job_name, job_path, parameters, node, state) values (?, ?, ?, ?, ?)'
        self.job_id = data_base.execute_sql_insert(
            sql,
            (
                job_name, job_path, parameters, node, 0
            )
        )

    def select_node(self, const):
        """Picking a node since parameters
        """
        if 'pulzar_data' in self.job_params['parameters']:
            # Send to the node where the data is
            data_base = DB(const.DB_PATH)
            composed_data = data_base.get_value(
                self.utils.encode_base_64(
                    self.job_params['parameters']['pulzar_data']), to_str=True
            )
            if composed_data is None:
                return None
            node = composed_data.split(',')[0].split(':')[0]
            return node.encode()
        else:
            node_utils = NodeUtils(const)
            return node_utils.pick_a_volume()

    def send_job(self, const):
        """Send job to the node selected

            params:
             - const (Constants)
        """
        # Scheduled job
        if 'scheduled' in self.job_params['parameters']:
            return self.register_scheduled_job(const.DB_JOBS)
        node = self.select_node(const)
        print('node', node)
        if node is None:
            return False
        print('Sending job to node ', node)
        # Register in data base
        self.register_job(const.DB_JOBS, node.decode())
        if self.job_id is None:
            return False
        self.job_params['job_id'] = self.job_id
        self.job_params['scheduled'] = 0
        request = CoreRequest(node.decode(), '9001', '/send_job')
        request.set_type(ReqType.POST)
        request.set_payload(self.job_params)
        job_response = request.make_request(json_request=True)
        if not job_response:
            # removing job
            self.unregister_job(const.DB_JOBS)
        return job_response

    def send_scheduled_job(self, const, parameters):
        """Send job to the node selected

            params:
             - const (Constants)
             - params: dict
        """
        node = self.select_node(const)
        print('node', node)
        print('parameters', parameters)
        if node is None:
            return False
        print('Sending job to node ', node)
        request = CoreRequest(node.decode(), '9001', '/send_job')
        request.set_type(ReqType.POST)
        request.set_payload(parameters)
        job_response = request.make_request(json_request=True)
        print(request.response)
        if not job_response:
            # removing job
            print('FALSE')
        return job_response
