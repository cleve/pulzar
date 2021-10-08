from time import sleep
from pulzarutils.utils import Utils
from pulzarutils.stream import Config
from pulzarutils.constants import Constants
from pulzarutils.logger import PulzarLogger
from pulzarcore.core_rdb import RDB
from pulzarcore.core_rabbit import Rabbit


class RegisterJob:
    """Class used to register jobs using subscriptor
    Run in node
    """
    def __init__(self):
        self.TAG = self.__class__.__name__
        self.logger = PulzarLogger(master=False)
        self.utils = Utils()
        self.config = Config(Constants.CONF_PATH)
        self.data_base = RDB(Constants.DB_NODE_JOBS)
        self.jobs_to_launch = []
        # Master configuration
        self.server_host = None
        self.server_port = None
        # Rabbit subcriber to jobs
        self.rabbit = Rabbit()

    def _checker(self, file_path, file_name):
        """Check path of job"""
        job_directory = self.config.get_config('jobs', 'dir')
        if job_directory is None:
            self.logger.debug(':{}:path -> {}'.format(self.TAG, 'First you need to set/create the job directory'))

        # check if the job exists
        path_to_search = job_directory + file_path + '/' + file_name + '.py'
        self.logger.debug(':{}:path -> {}'.format(self.TAG, path_to_search))
        return self.utils.file_exists(path_to_search)
            
    def _receiver_callback(self, ch, method, properties, body) -> None:
        """Register job in node
        """
        # Unpacking
        action, job_id, *arguments = body.decode().split(',')
        if job_id is None:
            print('Invalid job_id: ', job_id)
        if not self._checker(arguments[0], arguments[1]):
            self.logger.error(':{}:job {} does not exist'.format(self.TAG, arguments[1]))
            
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
    print('[REGISTER JOBS] Starting...')
    sleep(15)
    print('[REGISTER JOBS] READY')
    registron = RegisterJob()
    registron.register_job()

if __name__ == "__main__":
    main()