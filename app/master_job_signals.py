from pulzarutils.utils import Utils
from pulzarutils.stream import Config
from pulzarutils.constants import Constants
from pulzarutils.logger import PulzarLogger
from pulzarcore.core_rdb import RDB
from pulzarcore.core_rabbit import Rabbit


class MasterJobSignals:
    """Class used to register job finished in node
    """
    def __init__(self):
        self.TAG = self.__class__.__name__
        self.logger = PulzarLogger(master=False)
        self.utils = Utils()
        self.config = Config(Constants.CONF_PATH)
        self.data_base = RDB(Constants.DB_NODE_JOBS)
        # Publisher to notify finished jobs
        self.rabbit_node_notify = Rabbit('notify_jobs_ready')
        
    def _receiver_callback(self, ch, method, properties, body) -> None:
        """Register jobs in master
        """
        # Unpacking
        action, job_id, *arguments = body.decode().split(',')
        if not self.checker(arguments[0], arguments[1]):
            self.logger.error(':{}:job {} does not exist'.format(self.TAG, arguments[1]))
            raise Exception('Job does not exist')
        job_path = self.utils.join_path(arguments[0], arguments[1])
        if Constants.DEBUG:
            print('registering job', action, job_id, arguments)
        parameters = arguments[2]
        scheduled = int(arguments[3])
        self.logger.info(':{}:callback executed'.format(self.TAG, ))
        # Volume job database
        data_base = RDB(Constants.DB_NODE_JOBS)
        table = 'job'
        if scheduled == 1:
            table = 'schedule_job'
        sql = 'INSERT INTO {} (job_id, job_path, parameters, state, notification) values (?, ?, ?, ?, ?)'.format(
            table)
        register_id = data_base.execute_sql_insert(
            sql,
            (
                job_id, job_path, parameters, 0, 0
            )
        )
        if register_id == -1:
            raise Exception('Unexpected error registering job')

    def register_job(self):
        """Use message broker
        """
        # Subscribe to pulzar exchange
        self.rabbit_node_notify.receiver(self._receiver_callback)

def main():
    """Entrance
    """
    registron = MasterJobSignals()
    registron.register_job()

if __name__ == "__main__":
    main()