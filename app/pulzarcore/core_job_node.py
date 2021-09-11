from pulzarcore.core_rdb import RDB
from pulzarutils.utils import Utils
from pulzarutils.utils import Constants


class Job:
    """Schedule jobs
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
        if self.job_scheduled:
            table = 'schedule_job'
        sql = 'UPDATE {} SET ready = 2 WHERE id = {}'.format(
            self.job_id).format(table)
        data_base.execute_sql(
            sql
        )

    def register_job(self, path_db_jobs):
        """Register job in node

        Parameters
        ----------
        path_db_jobs : str
            File path to the job database

        Return
        ------
        ID : int
            ID of the record created
        """
        if Constants.DEBUG:
            print('registering job')
        parameters = self.utils.py_to_json(self.job_params)
        # Volume job database
        data_base = RDB(path_db_jobs)
        table = 'job'
        if self.job_scheduled:
            table = 'schedule_job'
        sql = 'INSERT INTO {} (job_id, job_path, parameters, state, notification) values (?, ?, ?, ?, ?)'.format(
            table)
        register_id = data_base.execute_sql_insert(
            sql,
            (
                self.job_id, self.job_path, parameters, 0, 0
            )
        )
        return register_id

    def schedule_job(self):
        """Schedule job
        """
        # Register in data base
        if self.register_job(Constants.DB_NODE_JOBS) is not None:
            return True
        return False
