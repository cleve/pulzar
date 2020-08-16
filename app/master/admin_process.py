from pulzarutils.utils import Utils
from pulzarcore.core_db import DB
from pulzarcore.core_rdb import RDB


class AdminProcess:
    def __init__(self, constants):
        self.const = constants
        self.utils = Utils()
        # DB of values already loaded
        self.db_volumes = DB(self.const.DB_VOLUME)
        # Complex response, store the info necessary.
        self.complex_response = {
            'action': None,
            'parameters': None,
            'volume': None
        }

    def process_request(self, url_path):
        # Get request type, checking for key value.
        regex_result = self.utils.get_search_regex(
            url_path, self.const.RE_ADMIN)
        if regex_result:
            try:
                self.complex_response['action'] = self.const.ADMIN
                call_path_list = regex_result.groups()[0].split('/')
                call_path_list = [x for x in call_path_list if x != '']
                print(call_path_list)
                # All node status
                if len(call_path_list) == 1 and call_path_list[0] == 'network':
                    nodes_info = []
                    nodes = self.db_volumes.get_keys_values(to_str=True)
                    current_datetime = self.utils.get_current_datetime()
                    for node in nodes:
                        node_name = node[0]
                        raw_split_info = node[1].split(':')
                        node_datetime = self.utils.get_datetime_from_string(
                            raw_split_info[3])
                        delta_t = current_datetime - node_datetime
                        nodes_info.append(
                            {
                                'node': node_name,
                                'percent': raw_split_info[0],
                                'load': raw_split_info[1],
                                'synch': True if delta_t.total_seconds() < 1200 else False
                            }
                        )

                    self.complex_response['parameters'] = self.utils.py_to_json(
                        nodes_info,
                        to_bin=True
                    )
                # Node status
                elif len(call_path_list) == 2 and call_path_list[0] == 'network':
                    node_to_search = self.utils.encode_str_to_byte(
                        call_path_list[1])
                    node = self.db_volumes.get_value(
                        node_to_search, to_str=True)
                    current_datetime = self.utils.get_current_datetime()
                    raw_split_info = node.split(':')
                    node_datetime = self.utils.get_datetime_from_string(
                        raw_split_info[3])
                    delta_t = current_datetime - node_datetime
                    get_result = {
                        'percent': raw_split_info[0],
                        'load': raw_split_info[1],
                        'synch': True if delta_t.total_seconds() < 1200 else False
                    }
                    self.complex_response['parameters'] = self.utils.py_to_json(
                        get_result, to_bin=True)

                # Jobs
                elif len(call_path_list) == 1 and call_path_list[0] == 'jobs':
                    data_base = RDB(self.const.DB_JOBS)
                    scheduled_job = []
                    pendings_jobs = []
                    ready_jobs = []
                    failed_jobs = []
                    # Get pending jobs
                    sql = 'SELECT id, job_name, parameters, node, creation_time, state FROM job WHERE state = 0'
                    rows = data_base.execute_sql_with_results(sql)
                    for pending in rows:
                        pendings_jobs.append({
                            'job_id': pending[0],
                            'job_name': pending[1],
                            'parameters': pending[2],
                            'node': pending[3],
                            'creation_time': pending[5]
                        })
                    # Get ready jobs
                    sql = 'SELECT id, job_name, parameters, node, creation_time, state FROM job WHERE state = 1'
                    rows = data_base.execute_sql_with_results(sql)
                    for ready in rows:
                        ready_jobs.append({
                            'job_id': ready[0],
                            'job_name': ready[1],
                            'parameters': ready[2],
                            'node': ready[3],
                            'creation_time': ready[5]
                        })
                    # Get failed jobs
                    sql = 'SELECT id, job_name, parameters, node, creation_time, state FROM job WHERE state = 2'
                    rows = data_base.execute_sql_with_results(sql)
                    for failed in rows:
                        failed_jobs.append({
                            'job_id': failed[0],
                            'job_name': failed[1],
                            'parameters': failed[2],
                            'node': failed[3],
                            'creation_time': failed[5]
                        })
                    # Get scheduled jobs
                    sql = 'SELECT job_id, job_name, parameters, creation_time, interval, time_unit, repeat, next_execution FROM schedule_job'
                    rows = data_base.execute_sql_with_results(sql)
                    for schedule in rows:
                        scheduled_job.append({
                            'job_id': schedule[0],
                            'job_name': schedule[1],
                            'parameters': schedule[2],
                            'creation_time': schedule[3],
                            'interval': schedule[4],
                            'time_unit': schedule[5],
                            'repeat': schedule[6],
                            'next_execution': schedule[7]
                        })
                    result = {
                        'pendings': pendings_jobs,
                        'ready': ready_jobs,
                        'failed': failed_jobs,
                        'scheduled': scheduled_job
                    }
                    self.complex_response['parameters'] = self.utils.py_to_json(
                        result, to_bin=True)

                # job details
                elif len(call_path_list) == 2 and call_path_list[0] == 'jobs':
                    data_base = RDB(self.const.DB_JOBS)
                    job_id = call_path_list[1]
                    # Getting details
                    sql = 'SELECT state FROM job WHERE id = {}'.format(job_id)
                    rows = data_base.execute_sql_with_results(sql)
                    if len(rows) == 0:
                        self.complex_response['action'] = self.const.KEY_NOT_FOUND
                        return self.complex_response
                    if rows[0][0] == 1:
                        table = 'successful_job'
                    elif rows[0][0] == 2:
                        table = 'failed_job'
                    sql = 'SELECT log, time, output FROM {} WHERE job_id = {}'.format(
                        table, job_id)
                    job_details = data_base.execute_sql_with_results(sql)
                    result = {
                        'job': job_id,
                        'log': job_details[0][0],
                        'time': job_details[0][1]
                    }
                    self.complex_response['parameters'] = self.utils.py_to_json(
                        result, to_bin=True)

                elif len(call_path_list) == 1 and call_path_list[0] == 'status':
                    db_master = DB(self.const.DB_PATH)
                    self.complex_response['parameters'] = self.utils.py_to_json(
                        db_master.get_stats(), to_bin=True)
                else:
                    self.complex_response['action'] = self.const.KEY_NOT_FOUND
                return self.complex_response

            except Exception as err:
                print('Error extracting key', err)
