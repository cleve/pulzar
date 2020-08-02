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

    def is_the_job_ok(self):
        """Should be at the end
        """
        return not self._failed_job

    def mark_as_failed(self):
        self._failed_job = True

    def add_log(self, message):
        self._log.append(message)

    def run_job(self) -> None:
        """Send job to be proccesed
        """
        pass

    def notification(self):
        """Notify to master
        """
        # Saving logs
        final_log = '\n'.join(self._log)
        sql = 'UPDATE job SET log = "{}" WHERE job_id = {}'.format(
            final_log, self._job_id)
        self.database.execute_sql(sql)
        # Notifications
        if self._notification_enabled:
            print('Sending notification...')
