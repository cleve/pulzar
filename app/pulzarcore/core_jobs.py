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
        self._log = []
        self._failed_job = False

        # log
        self.pulzar_register_parameters()

    def pulzar_register_parameters(self):
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
        # Saving logs
        final_log = '\n'.join(self._log)
        sql = 'UPDATE job SET log = ? WHERE job_id = {}'.format(
            self._job_id)
        self.database.execute_sql_insert(sql, (final_log,))
        # Notifications
        if self._notification_enabled:
            print('Sending notification...')
