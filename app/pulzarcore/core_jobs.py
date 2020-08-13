from pulzarutils.utils import Utils
from pulzarutils.utils import Constants
from pulzarcore.core_rdb import RDB


class CoreJobs:
    """Base class for job implementation
    """

    def __init__(self, parameters, notification=False):
        """Constructor
            arguments:
             - parameters (dict)
        """
        self.utils = Utils()
        self.const = Constants()
        self.database = RDB(self.const.DB_NODE_JOBS)
        self.parameters = parameters
        self._notification_enabled = notification
        self._job_id = parameters['job_id']
        self._start_time = self.utils.get_current_datetime()
        self._log = []
        self._failed_job = False
        self._pulzar_data_file_path = None

        # log
        self._pulzar_register_parameters()
        self._pulzar_get_data()

    def _pulzar_get_data(self):
        """Check file/config and assign it
        """
        if 'pulzar_data' in self.parameters:
            file_path = self.parameters['pulzar_data']
            abs_path = '/var/lib/pulzar/data/' + self.utils.encode_base_64(
                file_path, to_str=True)
            if self.utils.file_exists(abs_path):
                self._pulzar_data_file_path = abs_path
        print(self._pulzar_data_file_path)

    def pulzar_get_filepath(self):
        """Return filepath
        """
        return self._pulzar_data_file_path

    def _pulzar_register_parameters(self):
        if self.parameters:
            self.pulzar_add_log(
                self.utils.py_to_json(self.parameters)
            )

    def _pulzar_run_job(executor):
        """Decorator to handle job execution
        """

        def wrapper(self):
            print('Pulzar core executing')
            try:
                executor(self)
            except Exception as err:
                self._mark_as_failed()
                self.pulzar_add_log(str(err))
            self._pulzar_notification()
            return self.is_the_job_ok()
        return wrapper

    def is_the_job_ok(self):
        """Should be at the end
        """
        return not self._failed_job

    def _mark_as_failed(self):
        self._failed_job = True

    def pulzar_add_log(self, message):
        self._log.append(message)

    def _pulzar_notification(self):
        """Notify to master
        """
        job_table = 'job'
        if self._pulzar_job_type == 'scheduled':
            job_table = 'schedule_job'
        end_time = self.utils.get_current_datetime()
        delta = end_time - self._start_time
        # Saving logs
        final_log = '\n'.join(self._log)
        sql = 'UPDATE {} SET log = ?, duration = ? WHERE job_id = {}'.format(
            job_table, self._job_id)
        self.database.execute_sql_insert(
            sql, (final_log, delta.total_seconds()))

        # Notifications
        if self._notification_enabled:
            print('Sending notification...')
