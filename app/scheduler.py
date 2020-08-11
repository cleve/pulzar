import schedule
import time

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
        self.jobs_to_launch = []
        # Master configuration
        self.server_host = None
        self.server_port = None
        self.get_config()

    def _search_jobs(self):
        """Search job scheduled
        """
        sql = 'SELECT * FROM schedule_job WHERE scheduled = 0'
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

    def run_forever(self):
        while True:
            self._search_jobs()
            schedule.run_pending()
            time.sleep(60)


scheduler_object = Scheduler()
scheduler_object.run_forever()
