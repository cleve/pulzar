import requests

# Internal imports
from pulzarcore.core_db import DB
from pulzarutils.constants import Constants
from pulzarutils.utils import Utils
from pulzarutils.stream import Config


class TemporalCheck:
    """Proccess who check for files
    that needs to be deleted
    """

    def __init__(self):
        self.const = Constants()
        self.utils = Utils()
        self.temporal_files = DB(self.const.DB_NOT_PERMANENT)
        self.master_db = DB(self.const.DB_PATH)
        self.init_config()

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
            url='http://' + url + '/delete_key/' + key
        )
        # Delete temporal register
        if req.status_code >= 200 and req.status_code < 300:
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
                if self.const.DEBUG:
                    print('Key {} with time alive of {} days'.format(
                        self.utils.decode_base_64(bkey, to_str=True), delta))
                # Remove data
                if delta > days:
                    self.delete_request(bkey)


def main():
    """Entrance
    """
    temporal_checker = TemporalCheck()
    temporal_checker.start_process()


if __name__ == "__main__":
    main()
