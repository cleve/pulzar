import schedule
import time
import os
import importlib
from pulzarutils.utils import Utils
from pulzarutils.constants import Constants
from pulzarutils.constants import ReqType
from pulzarutils.node_utils import NodeUtils
from pulzarcore.core_rdb import RDB
from pulzarcore.core_db import DB
from pulzarcore.core_request import CoreRequest
from pulzarcore.core_job_master import Job


class Scheduler():
    def __init__(self):
        self.const = Constants()
        self.utils = Utils()
        self.schedule_data_base = RDB(self.const.DB_JOBS)
        self.max_jobs_running = 4
        self.jobs_to_launch = []

    def _process_params(self):
        """JSON to python objects
        """
        for job in self.jobs_to_launch:
            args = job['parameters']
            if args != '':
                job['parameters'] = self.utils.json_to_py(args)

    def _search_jobs(self):
        """Search job scheduled
        """
        limit = self.max_jobs_running - len(self.jobs_to_launch)
        sql = 'SELECT job_id, job_name, job_path, parameters, interval, time_unit, repeat FROM schedule_job WHERE scheduled = 0 LIMIT {}'.format(
            limit)
        rows = self.schedule_data_base.execute_sql_with_results(sql)
        for row in rows:
            print(row[3], type(row[3]))
            self.jobs_to_launch.append({
                'job_id': row[0],
                'job_name': row[1],
                'job_path': row[2],
                'parameters': row[3],
                'job_interval': row[4],
                'job_time_unit': row[5],
                'job_repeat': row[6]
            })

    def _notify_to_node(self, params):
        """Send the job to the node
        """
        job_object = Job(params)
        if job_object.send_scheduled_job(self.const, params):
            return True
        return False

    def _schedule_jobs(self):
        """Execute jobs selected
        """
        print('Schedule jobs', schedule.jobs)
        for iter_job in range(len(self.jobs_to_launch)):
            try:
                job = self.jobs_to_launch.pop()
                print('Scheduling', job['job_id'],
                      'located in ', job['job_path'])
                job['scheduled'] = 1
                schedule.every(1).minutes.do(self._notify_to_node, params=job)
                # mark as scheduled
                sql = 'UPDATE schedule_job SET scheduled = 1 WHERE job_id = {}'.format(
                    job['job_id'])
                print(sql)
                self.schedule_data_base.execute_sql(sql)
            except Exception as err:
                print('Error executing the job: ', err)

    def run_forever(self):
        while True:
            self._search_jobs()
            self._process_params()
            self._schedule_jobs()
            schedule.run_pending()
            time.sleep(1)


scheduler_object = Scheduler()
scheduler_object.run_forever()
