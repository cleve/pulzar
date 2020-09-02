from pulzarutils.utils import Utils
from pulzarutils.constants import ReqType
from pulzarutils.node_utils import NodeUtils
from pulzarutils.messenger import Messenger
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
        self.messenger = Messenger()

    def process_notification_request(self, url_path, query_string, env):
        """Processing job notification from node
            state = 1: succeful
            state = 2: error
        """
        try:
            body = Body()
            job_params = body.extract_params(env)
            # Main table
            table, id_table = ('job', 'id') if not job_params['scheduled'] else (
                'schedule_job', 'job_id')
            sql = 'UPDATE {} SET state = {} WHERE {} = {}'.format(
                table, job_params['state'], id_table, job_params['job_id'])
            update_rows_affected = self.data_base.execute_sql(sql)
            if update_rows_affected == 0:
                self.messenger.code_type = self.const.JOB_ERROR
                self.messenger.mark_as_failed()
                return self.messenger
            # Store log and time
            state = job_params['state']
            if int(state) == 1:
                table = 'successful_job'
                if job_params['scheduled']:
                    table = 'successful_schedule_job'
            elif state == 2:
                table = 'failed_job'
                if job_params['scheduled']:
                    table = 'failed_schedule_job'
            sql = 'INSERT INTO {} (job_id, log, time, output) VALUES (?, ?, ?, ?)'.format(
                table)
            insert_rows_affected = self.data_base.execute_sql_insert(
                sql, (job_params['job_id'],
                      job_params['log'],
                      job_params['time'],
                      job_params['output']
                      )
            )
            if insert_rows_affected > 0:
                self.messenger.code_type = self.const.JOB_RESPONSE
                self.messenger.set_message = 'ok'
            else:
                self.messenger.code_type = self.const.JOB_ERROR
                self.messenger.mark_as_failed()

        except Exception as err:
            print('Error process_notification_request', err)
            self.messenger.code_type = self.const.JOB_ERROR
            self.messenger.mark_as_failed()

        return self.messenger

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
                self.messenger.code_type = self.const.JOB_RESPONSE
                self.messenger.set_message = 'Job added with id ' + \
                    str(job_object.job_id)

            else:
                self.messenger.set_message = job_object.error_msg
                self.messenger.code_type = self.const.JOB_ERROR
                self.messenger.mark_as_failed()

        except Exception as err:
            print('Job_process_Error', err)
            self.messenger.code_type = self.const.JOB_ERROR
            self.messenger.mark_as_failed()
            self.messenger.set_message = str(err)

        return self.messenger
