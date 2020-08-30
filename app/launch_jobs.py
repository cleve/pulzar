import os
import importlib
from pulzarutils.utils import Utils
from pulzarutils.constants import Constants
from pulzarutils.constants import ReqType
from pulzarutils.stream import Config
from pulzarcore.core_rdb import RDB
from pulzarcore.core_request import CoreRequest


class LaunchJobs:
    """Handle job scheduled
    """

    def __init__(self):
        self.const = Constants()
        self.utils = Utils()
        self.data_base = RDB(self.const.DB_NODE_JOBS)
        self.jobs_to_launch = []
        # Master configuration
        self.server_host = None
        self.server_port = None
        self.get_config()
        self.search_pending_jobs()

    def get_config(self):
        """Configuration from ini file
        """
        server_config = Config(self.const.CONF_PATH)
        # Master url
        self.server_host = server_config.get_config('server', 'host')
        self.server_port = server_config.get_config('server', 'port')

    def notify_to_master(self, job_id, scheduled=False):
        """Sending the signal to master
        """
        # Recovering data of job
        table = 'job' if not scheduled else 'schedule_job'
        sql = 'SELECT log, duration, state, output FROM {} WHERE job_id = {} AND notification = 0'.format(
            table, job_id)
        row = self.data_base.execute_sql_with_results(sql)[0]

        payload = {
            'job_id': job_id,
            'log': row[0],
            'time': row[1],
            'state': row[2],
            'output': row[3],
            'scheduled': scheduled
        }
        req = CoreRequest(self.server_host, self.server_port,
                          '/notification_job')
        req.set_type(ReqType.POST)
        req.set_payload(payload)
        if req.make_request(json_request=True):
            # Update the state
            sql = 'UPDATE job SET notification = 1 WHERE job_id = {}'.format(
                job_id)
            self.data_base.execute_sql(sql)

    def process_params(self):
        """JSON to python objects
        """
        for job in self.jobs_to_launch:
            args = job['job_args']
            if args != '':
                job['job_args'] = self.utils.json_to_py(args)

    def mark_job(self, job_id, state, scheduled):
        """Mark a job if is ok or failed
        """
        status = 1 if state else 2
        table = 'job' if not scheduled else 'schedule_job'
        sql = 'UPDATE {} SET state = {} WHERE job_id = {}'.format(
            table, status, job_id)
        return self.data_base.execute_sql(sql) > 0

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
                job['job_args']['_pulzar_config'] = {
                    'scheduled': job['scheduled']}
                import_fly = importlib.import_module(custom_module)
                status = import_fly.execute(job['job_args'])
                # Report to master
                if self.mark_job(job['job_id'], status, job['scheduled']):
                    self.notify_to_master(job['job_id'], job['scheduled'])
            except Exception as err:
                print('Error executing the job: ', err)

    def search_jobs(self):
        """Search job scheduled
        """
        sql = 'SELECT * FROM job WHERE state = 0'
        rows = self.data_base.execute_sql_with_results(sql)
        for row in rows:
            self.jobs_to_launch.append({
                'job_id': row[0],
                'job_path': row[1],
                'job_args': row[2],
                'job_creation': row[4],
                'scheduled': False
            })
        sql = 'SELECT * FROM schedule_job WHERE state = 0'
        rows = self.data_base.execute_sql_with_results(sql)
        for row in rows:
            self.jobs_to_launch.append({
                'job_id': row[0],
                'job_path': row[1],
                'job_args': row[2],
                'job_creation': row[4],
                'scheduled': True
            })

    def search_pending_jobs(self):
        """Search job scheduled
        """
        sql = 'SELECT * FROM job WHERE state <> 0 AND notification = 0'
        rows = self.data_base.execute_sql_with_results(sql)
        for row in rows:
            self.notify_to_master(row[0])


def main():
    """Entrance
    """
    launcher = LaunchJobs()
    launcher.search_jobs()
    launcher.process_params()
    launcher.execute_jobs()


if __name__ == "__main__":
    main()
