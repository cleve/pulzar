from utils.utils import Utils
from utils.constants import Constants
from core.core_rdb import RDB


class LaunchJobs:
    """Handle job scheduled
    """

    def __init__(self):
        self.const = Constants()
        self.utils = Utils()
        self.data_base = RDB(self.const.DB_NODE_JOBS)
        self.jobs_to_launch = []


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



