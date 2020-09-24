from pulzarutils.utils import Utils
from pulzarutils.messenger import Messenger
from pulzarcore.core_rdb import RDB


class AdminJobs:
    def __init__(self, constants):
        self.const = constants
        self.utils = Utils()
        self.messenger = Messenger()

    def _scheduled_job_type(self, job_type, limit):
        data_base = RDB(self.const.DB_JOBS)
        result = []
        if job_type == 'failed':
            sql = """\
                SELECT 
                    sj.job_id,
                    sj.job_name,
                    sj.parameters,
                    sj.creation_time,
                    sj.interval,
                    sj.time_unit,
                    fsj.log,
                    fsj.output,
                    fsj.date_time,
                    sj.next_execution
                FROM schedule_job as sj
                INNER JOIN failed_schedule_job as fsj ON sj.job_id = fsj.job_id
                WHERE scheduled <> -2 ORDER BY sj.job_id DESC"""
        elif job_type == 'ok':
            sql = """\
                SELECT 
                    sj.job_id,
                    sj.job_name,
                    sj.parameters,
                    sj.creation_time,
                    sj.interval,
                    sj.time_unit,
                    ssj.log,
                    ssj.output,
                    ssj.date_time,
                    sj.next_execution
                FROM schedule_job as sj
                INNER JOIN successful_schedule_job as ssj ON sj.job_id = ssj.job_id
                WHERE scheduled <> -2 ORDER BY sj.job_id DESC"""

        if limit is not None:
            sql += ' LIMIT ' + str(limit)

        rows = data_base.execute_sql_with_results(sql)
        if len(rows) == 0:
            return result
        # Job executed correctly
        if len(rows) > 0:
            for row in rows:
                result.append({
                    'job_id': row[0],
                    'job_name': row[1],
                    'parameters': row[2],
                    'creation': row[3],
                    'interval': row[4],
                    'time_unit': row[5],
                    'log': row[6],
                    'output': row[7],
                    'datetime': row[8],
                    'next_execution': row[9]
                })
        return result

    def _scheduled_job_response(self, job_id, job_type, limit):
        """Get scheduled job information since all parameters
        """
        scheduled_job = []
        data_base = RDB(self.const.DB_JOBS)
        if job_id is None:
            # Only job list
            if job_type is not None:
                return self._scheduled_job_type(job_type, limit)
            # Get scheduled jobs
            sql = 'SELECT job_id, job_name, parameters, creation_time, interval, time_unit, repeat, next_execution, scheduled FROM schedule_job'
            if limit is not None:
                sql += ' LIMIT ' + str(limit)
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
                    'next_execution': schedule[7],
                    'state': 'canceled' if schedule[8] == -2 else 'scheduled'
                })
            return scheduled_job

        # Search job
        sql = 'SELECT job_id, job_path, job_name, next_execution, creation_time, scheduled FROM schedule_job WHERE job_id = {}'.format(
            job_id)
        if limit is not None:
            sql += ' LIMIT ' + str(limit)
        job_row = data_base.execute_sql_with_results(sql)
        if len(job_row) == 0:
            self.messenger.code_type = self.const.KEY_NOT_FOUND
            self.messenger.set_message = 'job id not found'
            return None

        result = {
            'job': job_id,
            'job_path': job_row[0][1],
            'job_name': job_row[0][2],
            'next_execution': job_row[0][3],
            'state': 'canceled' if job_row[0][5] == -2 else None,
            'last_executions': [],
            'creation': job_row[0][4],
        }
        self.messenger.code_type = self.const.JOB_DETAILS
        # Canceled, return
        if job_row[0][5] == -2:
            self.messenger.set_response(result)
            return self.messenger
        # Getting details
        sql = 'SELECT id, log, output, date_time FROM successful_schedule_job WHERE job_id = {} ORDER BY id DESC'.format(
            job_id)
        if limit is not None:
            sql += ' LIMIT ' + str(limit)
        rows = data_base.execute_sql_with_results(sql)
        # Job executed correctly
        if len(rows) > 0:
            for row in rows:
                result['last_executions'].append({
                    'state': 'ok',
                    'log': row[1],
                    'output': row[2],
                    'datetime': row[3]
                })
        else:
            sql = 'SELECT id, log, output, date_time FROM failed_schedule_job WHERE job_id = {} ORDER BY id DESC'.format(
                job_id)
            if limit is not None:
                sql += ' LIMIT ' + str(limit)
            rows = data_base.execute_sql_with_results(sql)
            if len(rows) > 0:
                for row in rows:
                    result['last_executions'].append({
                        'state': 'ok',
                        'log': row[1],
                        'output': row[2],
                        'datetime': row[3]
                    })
        return result

    def _job_response(self, job_id, job_type, limit):
        data_base = RDB(self.const.DB_JOBS)
        pendings_jobs = []
        ready_jobs = []
        failed_jobs = []
        # Get pending jobs
        data_base = RDB(self.const.DB_JOBS)
        if job_id is None:
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
            return {
                'pendings': pendings_jobs,
                'ready': ready_jobs,
                'failed': failed_jobs
            }

        sql = 'SELECT state FROM job WHERE id = {}'.format(job_id)
        rows = data_base.execute_sql_with_results(sql)
        if len(rows) == 0:
            self.messenger.code_type = self.const.KEY_NOT_FOUND
            self.messenger.set_message = 'job id not found'
            return None
        if rows[0][0] == 1:
            table = 'successful_job'
        elif rows[0][0] == 2:
            table = 'failed_job'
        sql = 'SELECT log, time, output FROM {} WHERE job_id = {}'.format(
            table, job_id)
        job_details = data_base.execute_sql_with_results(sql)
        return {
            'job': job_id,
            'log': job_details[0][0],
            'time': job_details[0][1]
        }

    def process_request(self, url_path):
        """Entrance for AdminJobs
        :param url_path:
        """
        # Get scheduled jobs.
        regex_result = self.utils.get_search_regex(
            url_path, self.const.RE_SCHED_JOB_INF)
        if regex_result:
            try:
                self.messenger.code_type = self.const.JOB_DETAILS
                # Type of request
                request_type, _, _, job_type, _, _, request_id, _, limit = regex_result.groups()
                # Filter request

                if request_type == 'scheduled_jobs':
                    self.messenger.set_response(
                        self._scheduled_job_response(request_id, job_type, limit))
                elif request_type == 'jobs':
                    self.messenger.set_response(
                        self._job_response(request_id, job_type, limit))
                return self.messenger
            except Exception as err:
                self.messenger.code_type = self.const.PULZAR_ERROR
                self.messenger.mark_as_failed()
                self.messenger.set_message = str(err)
        else:
            self.messenger.code_type = self.const.KEY_NOT_FOUND
            self.messenger.mark_as_failed()
            self.messenger.set_message = 'bad query'
        return self.messenger
