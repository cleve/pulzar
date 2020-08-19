from pulzarcore.core_rdb import RDB
from pulzarutils.utils import Utils


class Job:
    """Send tasks to the nodes
    """

    def __init__(self, job_id, job_path, job_params, job_scheduled):
        self.job_id = job_id
        self.job_path = job_path
        self.job_params = job_params
        self.job_scheduled = job_scheduled
        self.utils = Utils()

    def unregister_job(self, path_db_jobs):
        """Mark as failed job in master
        """
        print('uregistering job')
        # Master job database
        data_base = RDB(path_db_jobs)
        table = 'job'
        if self.schedule_job:
            table = 'schedule_job'
        sql = 'UPDATE {} SET ready = 2 WHERE id = {}'.format(
            self.job_id).format(table)
        data_base.execute_sql(
            sql
        )

    def register_job(self, path_db_jobs):
        """Register job in master
        """
        print('registering job')
        parameters = self.utils.py_to_json(self.job_params)
        # Master job database
        data_base = RDB(path_db_jobs)
        table = 'job'
        if self.schedule_job:
            table = 'schedule_job'
        sql = 'INSERT INTO {} (job_id, job_path, parameters, creation_time, state, notification) values (?, ?, ?, ?, ?, ?)'.format(
            table)
        register_id = data_base.execute_sql_insert(
            sql,
            (
                self.job_id, self.job_path, parameters, self.utils.get_current_datetime(), 0, 0
            )
        )
        return register_id

    def schedule_job(self, const):
        """Schedule job

            params:
             - const (Constants)
        """
        print('Sending job to node ')
        # Register in data base
        if self.register_job(const.DB_NODE_JOBS) is not None:
            return True
        return False
