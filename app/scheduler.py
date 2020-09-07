import schedule
import time
import os
import importlib
from pulzarutils.utils import Utils
from pulzarutils.constants import Constants
from pulzarutils.constants import ReqType
from pulzarutils.node_utils import NodeUtils
from pulzarcore.core_rdb import RDB
from pulzarcore.core_request import CoreRequest
from pulzarcore.core_job_master import Job


class Scheduler():
    def __init__(self):
        self.const = Constants()
        self.utils = Utils()
        self.schedule_data_base = RDB(self.const.DB_JOBS)
        self.max_jobs_running = 4
        self.jobs_to_launch = []
        self.days_of_retention = 90

    def init_state(self):
        """Restart schedule state at the begining
        """
        sql = 'UPDATE schedule_job SET scheduled = -1 WHERE scheduled = 1'
        self.schedule_data_base.execute_sql(sql)

    def _update_state(self):
        """Update next iteration
        """
        sql = 'SELECT job_id FROM schedule_job'
        rows = self.schedule_data_base.execute_sql_with_results(sql)
        for row in rows:
            for job in schedule.jobs:
                if row[0] in job.tags:
                    sql = 'UPDATE schedule_job SET next_execution = ? WHERE job_id = {}'.format(
                        row[0])
                    self.schedule_data_base.execute_sql_update(
                        sql, (self.utils.datetime_to_string(job.next_run, db_format=True),))

    def _schedule_job(self, parameters):
        self._notify_to_node(parameters)
        sql = 'UPDATE schedule_job SET scheduled = 0 WHERE job_id = {}'.format(
            parameters['job_id']
        )
        self.schedule_data_base.execute_sql(sql)

    def _resume_jobs(self):
        """Resume the jobs when the app crashes,
        is updated or rebooted
        """
        print('Resume jobs')
        sql = 'SELECT job_id, job_name, job_path, parameters, interval, time_unit, next_execution, repeat FROM schedule_job WHERE scheduled = -1 AND repeat = 1'
        pending_jobs = self.schedule_data_base.execute_sql_with_results(sql)
        for row in pending_jobs:
            job_id = row[0]
            job_name = row[1]
            job_path = row[2]
            parameters = row[3]
            interval = row[4]
            time_unit = row[5]
            next_execution = row[6]
            repeat = row[7]
            # Calculation of time
            current_datetime = self.utils.get_current_datetime()
            next_execution_datetime = self.utils.get_standard_datetime_from_string(
                next_execution)
            # Delta
            delta = current_datetime - next_execution_datetime
            # Not yet. This is the future
            print('INTERVAL: ', interval)
            if delta.days < 0:
                print('negative', delta)
                print('minutes', 10080 * time_unit)
                continue
            # Time units
            if interval == 'weeks':
                print(delta, current_datetime, next_execution_datetime)
                minutes_convertion = delta.seconds / 60
                # To minutes
                time_unit_to_minutes = 10080 * time_unit
                print(minutes_convertion, time_unit_to_minutes)
                # Pendings
                if minutes_convertion < int(time_unit_to_minutes):
                    # launch job
                    self._schedule_job({
                        'job_id': job_id,
                        'job_name': job_name,
                        'job_path': job_path,
                        'parameters': self.utils.json_to_py(parameters),
                        'job_interval': interval,
                        'job_time_unit': time_unit,
                        'job_repeat': repeat,
                        'scheduled': 1
                    })
                elif delta.days > 0 and minutes_convertion > int(time_unit):
                    sql = 'UPDATE schedule_job SET scheduled = 0 WHERE job_id = {}'.format(
                        job_id
                    )
                    self.schedule_data_base.execute_sql(sql)
            if interval == 'days':
                print(delta, current_datetime, next_execution_datetime)
                minutes_convertion = delta.seconds / 60
                # To minutes
                time_unit_to_minutes = 1440 * time_unit
                print(minutes_convertion, time_unit_to_minutes)
                # Pendings
                if minutes_convertion < int(time_unit_to_minutes):
                    # launch job
                    self._schedule_job({
                        'job_id': job_id,
                        'job_name': job_name,
                        'job_path': job_path,
                        'parameters': self.utils.json_to_py(parameters),
                        'job_interval': interval,
                        'job_time_unit': time_unit,
                        'job_repeat': repeat,
                        'scheduled': 1
                    })
                elif delta.days > 0 and minutes_convertion > int(time_unit):
                    sql = 'UPDATE schedule_job SET scheduled = 0 WHERE job_id = {}'.format(
                        job_id
                    )
                    self.schedule_data_base.execute_sql(sql)

            if interval == 'hours':
                print(delta, current_datetime, next_execution_datetime)
                minutes_convertion = delta.seconds / 60
                # To minutes
                time_unit_to_minutes = 60 * time_unit
                print(minutes_convertion, time_unit_to_minutes)
                # Pendings
                if minutes_convertion < int(time_unit_to_minutes):
                    # launch job
                    self._schedule_job({
                        'job_id': job_id,
                        'job_name': job_name,
                        'job_path': job_path,
                        'parameters': self.utils.json_to_py(parameters),
                        'job_interval': interval,
                        'job_time_unit': time_unit,
                        'job_repeat': repeat,
                        'scheduled': 1
                    })
                elif delta.days > 0 and minutes_convertion > int(time_unit):
                    sql = 'UPDATE schedule_job SET scheduled = 0 WHERE job_id = {}'.format(
                        job_id
                    )
                    self.schedule_data_base.execute_sql(sql)

            if interval == 'minutes':
                minutes_convertion = delta.seconds / 60
                # Pendings
                if minutes_convertion < int(time_unit):
                    # launch job
                    self._schedule_job({
                        'job_id': job_id,
                        'job_name': job_name,
                        'job_path': job_path,
                        'parameters': self.utils.json_to_py(parameters),
                        'job_interval': interval,
                        'job_time_unit': time_unit,
                        'job_repeat': repeat,
                        'scheduled': 1
                    })
                elif delta.days >= 0 and minutes_convertion > int(time_unit):
                    sql = 'UPDATE schedule_job SET scheduled = 0 WHERE job_id = {}'.format(
                        job_id
                    )
                    self.schedule_data_base.execute_sql(sql)

    def _process_params(self):
        """JSON to python objects
        """
        for job in self.jobs_to_launch:
            args = job['parameters']
            if args != '':
                job['parameters'] = self.utils.json_to_py(args)

    def _search_jobs(self):
        """Search for new jobs scheduled
        """
        limit = self.max_jobs_running - len(self.jobs_to_launch)
        sql = 'SELECT job_id, job_name, job_path, parameters, interval, time_unit, repeat FROM schedule_job WHERE scheduled = 0 LIMIT {}'.format(
            limit)
        rows = self.schedule_data_base.execute_sql_with_results(sql)
        for row in rows:
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
            # Update next iteration time
            self.update_next_execution_job(params['job_id'])
            return True

        return False

    def schedule_details(self, job_params, interval, time_unit):
        """Since parameter, schedule according it
            return schedule object
        """
        schedule_object = None
        if interval == 'minutes':
            schedule_object = schedule.every(int(time_unit)).minutes.do(
                self._notify_to_node, params=job_params)

        elif interval == 'hours':
            schedule_object = schedule.every(int(time_unit)).hours.do(
                self._notify_to_node, params=job_params)

        elif interval == 'days':
            schedule_object = schedule.every(int(time_unit)).days.do(
                self._notify_to_node, params=job_params)

        elif interval == 'weeks':
            schedule_object = schedule.every(int(time_unit)).weeks.do(
                self._notify_to_node, params=job_params)

        return schedule_object

    def update_next_execution_job(self, job_id):
        """Update the date of the next execution
        """
        time.sleep(5)
        for job in schedule.jobs:
            if job_id in job.tags:
                sql = 'UPDATE schedule_job SET next_execution = ? WHERE job_id = {}'.format(
                    job_id)
                self.schedule_data_base.execute_sql_update(
                    sql, (self.utils.datetime_to_string(job.next_run, db_format=True),))

    def _schedule_jobs(self):
        """Execute jobs selected
        """
        for iter_job in range(len(self.jobs_to_launch)):
            try:
                job = self.jobs_to_launch.pop()
                print('Scheduling', job['job_id'],
                      'located in ', job['job_path'])
                job['scheduled'] = 1
                # Getting configuration for schedule job.
                interval = job['job_interval']
                time_unit = job['job_time_unit']
                new_object = self.schedule_details(job, interval, time_unit)
                if new_object is None:
                    continue
                # Tagging the job with the ID
                new_object = new_object.tag(job['job_id'])
                next_execution = self.utils.datetime_to_string(
                    new_object.next_run, db_format=True)
                # mark as scheduled
                sql = 'UPDATE schedule_job SET scheduled = 1 , next_execution = ? WHERE job_id = {}'.format(
                    job['job_id'])
                self.schedule_data_base.execute_sql_update(
                    sql, (next_execution,))
            except Exception as err:
                print('Error executing the job: ', err)

    def run_forever(self):
        while True:
            self._resume_jobs()
            self._search_jobs()
            self._update_state()
            self._process_params()
            self._schedule_jobs()
            schedule.run_pending()
            time.sleep(20)


def main():
    """Entrance
    """
    scheduler_object = Scheduler()
    scheduler_object.init_state()
    scheduler_object.run_forever()


if __name__ == "__main__":
    main()
