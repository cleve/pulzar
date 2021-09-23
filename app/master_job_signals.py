from pulzarutils.utils import Utils
from pulzarutils.stream import Config
from pulzarutils.constants import Constants
from pulzarutils.logger import PulzarLogger
from pulzarcore.core_rdb import RDB
from pulzarcore.core_rabbit import Rabbit


class MasterJobSignals:
    """Class used to register job finished in node
    Run in master
    """
    def __init__(self):
        self.TAG = self.__class__.__name__
        self.logger = PulzarLogger(master=False)
        self.utils = Utils()
        self.config = Config(Constants.CONF_PATH)
        self.data_base = RDB(Constants.DB_JOBS)
        # Publisher to notify finished jobs
        self.rabbit_node_notify = Rabbit('notify_jobs_ready')
    
    def _validate_params(self, byte_string):
        """Validate values allowed
        
        Parameters
        ----------
        byte_string : bstring
        """
        # TODO: Validation
        pass
        
    def _receiver_callback(self, ch, method, properties, body) -> None:
        """Register jobs in master using the string body format:

            NOTIFY_JOB,job_id,log,output,time(s),
            job_ok[True,False],notification,scheduled[0,1],

            state = 0: pending
            state = 1: succeful
            state = 2: error
        """
        # Unpacking
        action, job_id, *arguments, scheduled = body.decode().split('-sep-')
        if Constants.DEBUG:
            print('updating job', action, job_id, arguments)

        if int(job_id) == -1:
            print('Invalid job_id')
            return
        # Main table
        table, id_table = ('job', 'id') if int(scheduled) == 0 else (
            'schedule_job', 'job_id')
        if table == 'job':
            current_datetime_utc = self.utils.get_current_datetime_utc(
                to_string=True, db_format=True)
            
            sql = 'UPDATE {} SET state = {}, creation_time = ? WHERE {} = {}'.format(
                table, arguments[3], id_table, job_id)

            update_rows_affected = self.data_base.execute_sql_update(
                sql, (current_datetime_utc,))
        else:
            sql = 'UPDATE {} SET state = {} WHERE {} = {}'.format(
                table, arguments[3], id_table, job_id)
            update_rows_affected = self.data_base.execute_sql(sql)

        if update_rows_affected == 0:
            raise Exception('Error receiving job signal')

        # Store log and time
        state = arguments[3]
        # Backward compatibility
        if isinstance(state, str):
            state = 1 if state == '1' else 2
        else:    
            state = int(arguments[3])
        # Datetime in UTC
        current_datetime_utc = self.utils.get_current_datetime_utc(
            to_string=True, db_format=True)
        if state == 1:
            table = 'successful_job'
            if int(scheduled) == 1:
                table = 'successful_schedule_job'
        elif state == 2:
            table = 'failed_job'
            if int(scheduled) == 1:
                table = 'failed_schedule_job'
        sql = 'INSERT INTO {} (job_id, log, time, output, date_time) VALUES (?, ?, ?, ?, ?)'.format(
            table)
        insert_rows_affected = self.data_base.execute_sql_insert(
            sql, (job_id,
                    arguments[0],
                    arguments[2],
                    arguments[1],
                    current_datetime_utc
                    )
        )
        self.logger.info(':{}:callback executed'.format(self.TAG, ))

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