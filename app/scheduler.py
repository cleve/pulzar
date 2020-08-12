import schedule
import time
import os
import importlib
from pulzarutils.utils import Utils
from pulzarutils.constants import Constants
from pulzarutils.constants import ReqType
from pulzarutils.stream import Config
from pulzarcore.core_rdb import RDB
from pulzarcore.core_request import CoreRequest
from launch_jobs import LaunchJobs


class Scheduler(LaunchJobs):
    def __init__(self):
        self.const = Constants()
        self.utils = Utils()
        self.schedule_data_base = RDB(self.const.DB_NODE_JOBS)
        self.max_jobs_running = 4
        self.jobs_to_launch = []
        # Master configuration
        self.server_host = None
        self.server_port = None
        self.get_config()

    def _search_jobs(self):
        """Search job scheduled
        """
        limit = self.max_jobs_running - len(self.jobs_to_launch)
        sql = 'SELECT * FROM schedule_job WHERE scheduled = 0 LIMIT {}'.format(
            limit)
        rows = self.schedule_data_base.execute_sql_with_results(sql)
        for row in rows:
            self.jobs_to_launch.append({
                'job_id': row[0],
                'job_path': row[1],
                'job_args': row[2],
                'job_creation': row[3],
                'job_interval': row[4],
                'job_time_unit': row[5],
                'job_repeat': row[6]
            })

    def _schedule_jobs(self):
        """Execute jobs selected
        """
        print('Schedule jobs', schedule.jobs)
        for iter_job in range(len(self.jobs_to_launch)):
            try:
                job = self.jobs_to_launch.pop()
                print('Scheduling', job['job_id'],
                      'located in ', job['job_path'])
                custom_module = os.path.splitext(job['job_path'])[
                    0].replace('/', '.')
                job['job_args']['job_id'] = job['job_id']
                job['job_args']['pulzar_type'] = 'scheduled'
                import_fly = importlib.import_module(custom_module)
                schedule.every(1).minutes.do(
                    import_fly.execute, arguments=job['job_args'])
                # mark as scheduled
                sql = 'UPDATE schedule_job SET scheduled = 1 WHERE job_id = {}'.format(
                    job['job_id'])
                self.schedule_data_base.execute_sql(sql)
                # if self.mark_job(job['job_id'], status):
                #    self.notify_to_master(job['job_id'])
            except Exception as err:
                print('Error executing the job: ', err)

    def run_forever(self):
        while True:
            self._search_jobs()
            self.process_params()
            self._schedule_jobs()
            schedule.run_pending()
            time.sleep(160)


scheduler_object = Scheduler()
scheduler_object.run_forever()
