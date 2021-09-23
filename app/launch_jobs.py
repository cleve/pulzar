import os
import importlib
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from pulzarutils.utils import Utils
from pulzarutils.constants import Constants
from pulzarutils.logger import PulzarLogger
from pulzarutils.stream import Config
from pulzarcore.core_rdb import RDB


class LaunchJobs:
    """Launch jobs in nodes
        - Scheduled
        - Single execution

        Script launched in nodes
    """

    def __init__(self):
        self.TAG = self.__class__.__name__
        self.logger = PulzarLogger(master=False)
        self.utils = Utils()
        self.data_base = RDB(Constants.DB_NODE_JOBS)
        self.jobs_to_launch = []
        # For threads.
        self.executor = ThreadPoolExecutor(max_workers=5, thread_name_prefix=f'{self.TAG}Executor')
        self.futures = []
        self.futures_ref = {}
        # Master configuration
        self.server_host = None
        self.server_port = None
        # Where the jobs will be placed
        self.job_directory = None
        self._get_config()
        self.days_of_retention = 90
        

    def _get_config(self):
        """Configuration from ini file
        """
        server_config = Config(Constants.CONF_PATH)
        # Retention
        self.days_of_retention = int(server_config.get_config(
            'general', 'retention_policy'))
        # Master url
        self.server_host = server_config.get_config('server', 'host')
        self.server_port = server_config.get_config('server', 'port')
        # Set job directory
        self.job_directory = server_config.get_config('jobs', 'dir')

    def _retention_policy(self):
        """Delete data since the policy configured under:
            config/server.conf
        """
        # Scheduled successful jobs
        date_diff = self.utils.get_date_days_diff(
            days=-1*self.days_of_retention, to_string=True)
        # Failed jobs
        sql = 'DELETE FROM schedule_job WHERE creation_time < {}'.format(
            date_diff)
        self.data_base.execute_sql(sql)

        # Regular jobs
        sql = 'DELETE FROM job WHERE creation_time < {}'.format(
            date_diff)
        self.data_base.execute_sql(sql)

    def _job_executor(self, obj, job_id, scheduled) -> None:
        """Execute object into the pool

        Parameters
        ----------
        obj : class
            The object to be executed
        """
        future = self.executor.submit(obj)
        self.futures.append(future)
        self.futures_ref.setdefault(id(future), [job_id, scheduled])
        
    def process_params(self):
        """JSON to python objects
        """
        for job in self.jobs_to_launch:
            args = job['job_args']
            if args != '':
                job['job_args'] = self.utils.json_to_py(args)

    def _mark_job(self, job_id, state, scheduled, log_msg=None) -> bool:
        """Mark a job if is ok or failed
        Parameters
        ----------
        job_id : int
            Job ID
        state: bool
            True for successful or Flase for failed job
        scheduled: str
            two types: schedule_job or job
        log_msg : str, None default
            Force a message. ex: syntax error
        
        Return
        ------
        bool : True for rows affected
        """
        if state is None:
            return False
        status = 1 if state else 2
        table = 'job' if not scheduled else 'schedule_job'
        if log_msg is None:
            sql = 'UPDATE {} SET state = ?, attempt = ? WHERE job_id = ?'.format(
                table)
            return self.data_base.execute_sql_update(sql, (status, 1, job_id)) > 0
        else:
            sql = 'UPDATE {} SET state = ?, log = ?, attempt = ? WHERE job_id = ?'.format(
                table)
            return self.data_base.execute_sql_update(sql, (status, log_msg, 1, job_id)) > 0
    
    def check_executors(self) -> None:
        """Check status and results
        """
        self.logger.info(f'{self.TAG}::futureRef:{self.futures_ref}')
        for future in as_completed(self.futures):
            self.logger.info(f'{self.TAG}::{future.__class__.__name__}::{id(future)}::{future.running()}')
            try:
                future_info = self.futures_ref.get(id(future))
                if future_info is None:
                    continue
                job_id, scheduled = future_info[0], future_info[1]
                if self._mark_job(job_id, future.result(), scheduled):
                    self.futures_ref.pop(id(future), None)
            except BaseException as err:
                self.logger.info(f'{self.TAG}::future: {id(future)}')
    
    def execute_jobs(self):
        """Execute jobs selected
        """
        if self.job_directory is None:
            raise Exception('First you need to set/create the job directory')

        for job in self.jobs_to_launch:
            try:
                # Rebuild the real path
                complete_path = self.job_directory + job.get('job_path')
                if Constants.DEBUG:
                    print('Launching', job.get('job_id'),
                        'located in ', complete_path)
                custom_module = os.path.splitext(complete_path)[
                    0].replace('/', '.')
                class_name = custom_module.split('.')[-1].capitalize()
                job['job_args']['job_id'] = job.get('job_id')
                job['job_args']['_pulzar_config'] = {
                    'scheduled': job['scheduled']
                }
                # Import module and method execute.
                self.logger.info(':{}:importing module -> {}'.format(self.TAG, custom_module))
                import_fly = importlib.import_module(custom_module)
                job_class = getattr(import_fly, class_name)
                job_object = job_class(job['job_args'])
                self._job_executor(job_object.execute, job.get('job_id'), job.get('scheduled'))
                
            except Exception as err:
                self.logger.exception(':{}:{}'.format(self.TAG, err))
                
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

def main():
    """Entrance
    """
    launcher = LaunchJobs()
    launcher.search_jobs()
    launcher.process_params()
    launcher.execute_jobs()
    launcher.check_executors()
    # Retention
    launcher._retention_policy()


if __name__ == "__main__":
    main()
