import os
import importlib
from pulzarutils.utils import Utils
from pulzarutils.constants import Constants
from pulzarcore.core_rdb import RDB


class LaunchJobs:
    """Handle job scheduled
    """

    def __init__(self):
        self.const = Constants()
        self.utils = Utils()
        self.data_base = RDB(self.const.DB_NODE_JOBS)
        self.jobs_to_launch = []

    def notify_to_master(self):
        pass

    def process_params(self):
        """JSON to python objects
        """
        for job in self.jobs_to_launch:
            args = job['job_args']
            if args != '':
                job['job_args'] = self.utils.json_to_py(args)

    def mark_job(self, job_id, state):
        """Mark a job if is ok or failed
        """
        status = 1 if state else 2
        sql = 'UPDATE job SET ready = {} WHERE job_id = {}'.format(
            status, job_id)
        self.data_base.execute_sql(sql)

    def execute_jobs(self):
        """Execute jobs selected
        """
        for job in self.jobs_to_launch:
            try:
                print('Launching', job['job_id'],
                      'located in ', job['job_path'])
                custom_module = os.path.splitext(job['job_path'])[
                    0].replace('/', '.')
                job['job_args']['job_id'] = job['job_id']
                import_fly = importlib.import_module(custom_module)
                status = import_fly.execute(job['job_args'])
                self.mark_job(job['job_id'], status)
            except Exception as err:
                print('Error executing the job: ', err)

    def search_jobs(self):
        """Search job scheduled
        """
        sql = 'SELECT * FROM job WHERE ready = 0'
        rows = self.data_base.execute_sql_with_results(sql)
        for row in rows:
            self.jobs_to_launch.append({
                'job_id': row[0],
                'job_path': row[1],
                'job_args': row[2],
                'job_creation': row[4]
            })


launcher = LaunchJobs()
launcher.search_jobs()
launcher.process_params()
launcher.execute_jobs()
