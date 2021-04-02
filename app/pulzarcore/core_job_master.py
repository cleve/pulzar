from pulzarcore.core_request import CoreRequest
from pulzarcore.core_rdb import RDB
from pulzarcore.core_db import DB
from pulzarutils.node_utils import NodeUtils
from pulzarutils.constants import ReqType
from pulzarutils.constants import Constants
from pulzarutils.utils import Utils


class Job:
    """Send jobs to the nodes
    """

    def __init__(self, job_params, url_path, logger):
        """Constructor

        Parameters
        ----------
        job_params : dict
            Dictionary with all the parameters
        
        url_path: str
            Full path to the job
        
        logger : Logger
            Logger object
        """
        self.TAG = self.__class__.__name__
        self.job_params = job_params
        self.url_path = url_path
        self.logger = logger
        self.utils = Utils()
        self.job_id = None
        self.volume_port = None
        self.error_msg = ''
        self.scheduler_checker = {
            'minutes': (5, 59),
            'hours': (1, 23),
            'days': (1, 31),
            'weeks': (1, 4)
        }
        # Passport to authorize the request in nodes
        self.passport = self.utils.get_passport()

    def unregister_job(self, path_db_jobs):
        """Mark as failed job in master
        """
        self.logger.debug(':{}:uregistering job'.format(self.TAG))
        # Master job database
        data_base = RDB(path_db_jobs)
        sql = 'UPDATE job SET state = 2 WHERE id = {}'.format(self.job_id)
        data_base.execute_sql(
            sql
        )

    def register_scheduled_job(self, path_db_jobs):
        """Register schedule job in master
        """
        self.logger.debug(':{}:registering scheduled job'.format(self.TAG))
        job_path = self.job_params['job_path']
        job_name = self.job_params['job_name']

        # Scheduler
        scheduler_object = self.job_params['parameters']['scheduled']
        self.logger.debug(scheduler_object)
        # Checking scheduler options
        if scheduler_object['interval'].lower() not in self.scheduler_checker:
            return False

        # Other parameters
        interval = scheduler_object['interval']
        time_unit = int(scheduler_object['time_unit'])
        if time_unit < self.scheduler_checker[interval.lower()][0] or time_unit > self.scheduler_checker[interval.lower()][1]:
            self.error_msg = 'interval not allowed for the time_unit'
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
        job_path = self.job_params['job_path']
        job_name = self.job_params['job_name']
        parameters = self.utils.py_to_json(self.job_params['parameters'])
        # Master job database
        data_base = RDB(path_db_jobs)
        sql = 'INSERT INTO job (job_name, job_path, parameters, creation_time, node, state) values (?, ?, ?, ?, ?, ?)'
        self.job_id = data_base.execute_sql_insert(
            sql, (
                job_name,
                job_path,
                parameters,
                self.utils.get_current_datetime_utc(
                    to_string=True, db_format=True),
                node,
                0
            )
        )

    def _select_node(self):
        """Picking a node since parameters

        The key provided in the pulzar_data key will be 
        searched and the node with the data will be selected
        to run the job. If the key pulzar_data is not present,
        a node with less workload will be selected.

        Return
        ------
        barray : node selected
        """
        node_utils = NodeUtils()
        self.volume_port = node_utils.get_port()
        if self.job_params.get('parameters').get('pulzar_data') is not None:
            # Send to the node where the data is
            data_base = DB(Constants.DB_PATH)
            composed_data = data_base.get_value(
                self.utils.encode_base_64(
                    self.job_params.get('parameters').get('pulzar_data')), to_str=True
            )
            if composed_data is None:
                return None
            node = composed_data.split(',')[0].split(':')[0]
            return node.encode()
        else:
            return node_utils.pick_a_volume2(self.url_path)
    
    def send_job(self):
        """Send job to the node selected

        Return
        ------
        Success : bool
            True if the job was sent correctly, False if not
        """
        # Scheduled job
        if 'scheduled' in self.job_params['parameters']:
            return self.register_scheduled_job(Constants.DB_JOBS)
        node = self._select_node()
        if node is None:
            self.logger.error(':{}:empty node'.format(self.TAG))
            return False
        self.logger.debug(':{}:Sending job to node -> {}'.format(self.TAG, node))
        # Register in data base
        self.register_job(Constants.DB_JOBS, node.decode())
        if self.job_id is None:
            return False
        self.job_params['job_id'] = self.job_id
        self.job_params['scheduled'] = 0
        request = CoreRequest(node.decode(), self.volume_port, '/send_job')
        request.set_type(ReqType.POST)
        request.set_payload(self.job_params)
        request.add_header({Constants.PASSPORT: self.passport})
        job_response = request.make_request(json_request=True)
        if not job_response:
            # removing job
            self.unregister_job(Constants.DB_JOBS)
            self.logger.error(':{}:could not communicate with node'.format(self.TAG))
            self.error_msg = 'could not communicate with node'
        elif job_response and request.json_response['status'] == 'ko':
            self.logger.error(':{}:{}'.format(self.TAG, request.json_response['msg']))
            self.error_msg = request.json_response['msg']
            self.unregister_job(Constants.DB_JOBS)
            return False
        return job_response

    def send_scheduled_job(self, parameters) -> bool:
        """Send scheduled job to the node selected

        Return
        ------
        bool : Successful or not
        """
        node = self._select_node()
        if Constants.DEBUG:
            print('node', node)
            print('port', self.volume_port)
            print('parameters', parameters)
        if node is None:
            return False
        request = CoreRequest(node.decode(), self.volume_port, '/send_job')
        request.set_type(ReqType.POST)
        request.set_payload(parameters)
        request.add_header({Constants.PASSPORT: self.passport})
        job_response = request.make_request(json_request=True)
        if Constants.DEBUG:
            print('Sending job to node ', node)
            print('response: ', request.response)
        if not job_response:
            # removing job
            print('FALSE response')
        return job_response
