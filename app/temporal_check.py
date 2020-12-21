import requests

# Internal imports
from pulzarcore.core_db import DB
from pulzarcore.core_rdb import RDB
from pulzarutils.constants import Constants
from pulzarutils.utils import Utils
from pulzarutils.stream import Config
from pulzarutils.logger import PulzarLogger


class TemporalCheck:
    """Proccess who check for files
    that needs to be deleted
    """

    def __init__(self):
        self.TAG = self.__class__.__name__
        self.const = Constants()
        self.logger = PulzarLogger(self.const)
        self.utils = Utils()
        self.temporal_files = DB(self.const.DB_NOT_PERMANENT)
        self.master_db = DB(self.const.DB_PATH)
        self.schedule_data_base = RDB(self.const.DB_JOBS)
        self.days_of_retention = 90
        self.init_config()

    def retention_policy(self):
        """Delete data since the policy
        """
        # Get retention policy from configuration
        server_config = Config(self.const.CONF_PATH)
        self.days_of_retention = int(server_config.get_config(
            'general', 'retention_policy'))
        # Canceled schedule jobs
        date_diff = self.utils.get_date_days_diff(
            days=-1*self.days_of_retention, to_string=True)
        sql = "DELETE FROM schedule_job WHERE next_execution < '{}' AND scheduled = -2".format(
            date_diff)
        self.schedule_data_base.execute_sql(sql)
        # Scheduled successful jobs
        date_diff = self.utils.get_date_days_diff(
            days=-1*self.days_of_retention, to_string=True)
        sql = "DELETE FROM successful_schedule_job WHERE creation_time < '{}'".format(
            date_diff)
        self.schedule_data_base.execute_sql(sql)
        # Failed jobs
        sql = "DELETE FROM failed_schedule_job WHERE creation_time < '{}'".format(
            date_diff)
        self.schedule_data_base.execute_sql(sql)
        # Regular jobs
        sql = "DELETE FROM job WHERE creation_time < '{}'".format(
            date_diff)
        self.schedule_data_base.execute_sql(sql)

    def init_config(self):
        """Getting server information
        """
        server_config = Config(self.const.CONF_PATH)
        self.master_url = server_config.get_config('server', 'host')
        self.master_port = server_config.get_config('server', 'port')

    def delete_request(self, bkey):
        """Delete the key and from the temporal register
        """
        key = self.utils.decode_base_64(bkey, True)
        url = self.master_url + ':' + self.master_port + '/'
        req = requests.delete(
            url='http://' + url + '/delete_key' + key
        )
        # Delete temporal register
        self.logger.info(':{}:deleting... code -> {}'.format(self.TAG, req.status_code))
        if req.status_code >= 200 and req.status_code < 300:
            message = req.json()
            self.logger.info(':{}:deleting response -> {}'.format(self.TAG, req.text))
            if message['status'] == 'ok':
                self.temporal_files.delete_value(bkey)

    def start_process(self):
        """Review files and delete it if match with the criteria
        """
        current_time = self.utils.get_current_datetime()
        with self.temporal_files.get_cursor_iterator() as txn:
            for _, data in enumerate(txn.cursor().iternext(keys=True, values=True)):
                bkey = data[0]
                days = int(data[1].decode())
                if days < 0:
                    continue

                # Get data from master
                master_value = self.master_db.get_value(bkey, True)
                if master_value is None:
                    # If is not present, delete it.
                    self.temporal_files.delete_value(bkey)
                    return
                value_datetime = self.utils.get_datetime_from_string(
                    master_value.split(',')[1])
                delta = (current_time - value_datetime).days
                self.logger.debug(':{}:Key {} with time alive of {} days and delta is {}'.format(
                        self.TAG,
                        self.utils.decode_base_64(bkey, to_str=True),
                        days,
                        delta
                    )
                )
                # Remove data
                if delta > days:
                    self.delete_request(bkey)


def main():
    """Entrance
    """
    temporal_checker = TemporalCheck()
    temporal_checker.start_process()
    temporal_checker.retention_policy()


if __name__ == "__main__":
    main()
