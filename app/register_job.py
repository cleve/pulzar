from pulzarutils.utils import Utils
from pulzarutils.constants import Constants
from pulzarutils.logger import PulzarLogger
from pulzarcore.core_rdb import RDB
from pulzarcore.core_rabbit import Rabbit


class RegisterJob:
    """Class used to register jobs using subscriptor
    """
    def __init__(self):
        self.TAG = self.__class__.__name__
        self.logger = PulzarLogger(master=False)
        self.utils = Utils()
        self.data_base = RDB(Constants.DB_NODE_JOBS)
        self.jobs_to_launch = []
        # Master configuration
        self.server_host = None
        self.server_port = None
        # Rabbit subcriber to jobs
        self.rabbit = Rabbit()
        # Publisher to master for finished jobs
        self.rabbit_notify = Rabbit()

    def _receiver_callback(self, ch, method, properties, body) -> None:
        """Register job in node
        """
        # Unpacking
        action, job_id, *arguments = body.decode().split(',')
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
        self.rabbit.receiver(self._receiver_callback)

def main():
    """Entrance
    """
    registron = RegisterJob()
    registron.register_job()

if __name__ == "__main__":
    main()