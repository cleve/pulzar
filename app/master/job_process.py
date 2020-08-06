from pulzarutils.utils import Utils
from pulzarutils.constants import ReqType
from pulzarutils.node_utils import NodeUtils
from pulzarcore.core_request import CoreRequest
from pulzarcore.core_rdb import RDB
from pulzarcore.core_job_master import Job
from pulzarcore.core_body import Body


class JobProcess:
    """Main class to handle jobs
    """

    def __init__(self, constants):
        self.const = constants
        self.utils = Utils()
        self.data_base = RDB(self.const.DB_JOBS)
        self.complex_response = {
            'action': None,
            'parameters': None,
            'volume': None
        }

    def process_notification_request(self, url_path, query_string, env):
        """Processing job notification from node
            state = 1: succeful
            state = 2: error
        """
        try:
            body = Body()
            job_params = body.extract_params(env)
            print('params:', job_params)
            # Main table
            sql = 'UPDATE job SET state = {} WHERE id = {}'.format(
                job_params['state'], job_params['job_id'])
            rows_affected = self.data_base.execute_sql(sql)
            # Store log and time
            state = job_params['state']
            if state == 1:
                table = 'successful_job'
            elif state == 2:
                table = 'failed_job'
            sql = 'INSERT INTO {} (job_id, log, time) VALUES ({}, "{}", {})'.format(
                table, job_params['job_id'], job_params['log'], job_params['time'])
            rows_affected = self.data_base.execute_sql(sql)
            if rows_affected > 0:
                self.complex_response['action'] = self.const.JOB_RESPONSE
                self.complex_response['parameters'] = b'ok'
            else:
                self.complex_response['action'] = self.const.JOB_ERROR

        except Exception as err:
            print('Error process_notification_request', err)
            self.complex_response['action'] = self.const.JOB_ERROR

        return self.complex_response

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
                self.complex_response['parameters'] = (
                    'Job added with id ' + str(job_object.job_id)).encode()
            else:
                self.complex_response['action'] = self.const.JOB_ERROR

        except Exception as err:
            print('Error extracting keywerwe', err)
            self.complex_response['action'] = self.const.JOB_ERROR

        return self.complex_response
