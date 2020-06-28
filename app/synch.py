from core.core_request import CoreRequest
from utils.utils import Utils
from utils.constants import Constants
from utils.constants import ReqType
from core.core_db import DB
from utils.stream import Config


class Synchro:
    """Check synchro between volume and master
    """

    def __init__(self):
        self.const = Constants()
        self.utils = Utils()
        self.db_stats = DB(self.const.DB_STATS)
        self.db_backup = DB(self.const.DB_BACKUP)
        self.volume_host = None
        self.server_host = None
        self.server_port = None
        self.volume_port = None
        self.backup_chunk = None
        self.restored_ready = None
        self.mark_of_local_verification = b'varidb_execute_file_verification'
        # Init main variables
        self.get_config()
        self.local_verificator2()

    def get_config(self):
        """Configuration from ini file
        """
        server_config = Config(self.const.CONF_PATH)
        self.volume_dir = server_config.get_config('volume', 'dir')
        self.volume_host = self.db_stats.get_value(
            self.utils.encode_str_to_byte(self.const.SERVER_NAME))
        self.restored_ready = self.db_stats.get_value(
            self.utils.encode_str_to_byte('restored'))
        self.volume_port = server_config.get_config('volume', 'port')
        self.backup_chunk = int(
            server_config.get_config('volume', 'backup_chunk'))
        # Master url
        self.server_host = server_config.get_config('server', 'host')
        self.server_port = server_config.get_config('server', 'port')

    def create_restore_DB(self):
        for file_item in self.utils.get_all_files(self.volume_dir + '/**'):
            if file_item == self.volume_dir + '/':
                continue
            file_item_byte = self.utils.encode_str_to_byte(
                self.utils.get_base_name_from_file(file_item))
            self.db_backup.update_or_insert_value(
                file_item_byte,
                b'0'
            )

    def count_files_synchronized(self):
        counter = 0
        for file_item in self.utils.get_all_files(self.volume_dir + '/**'):
            if file_item == self.volume_dir + '/':
                continue
            file_item_byte = self.utils.encode_str_to_byte(
                self.utils.get_base_name_from_file(file_item))
            if self.db_backup.get_equal_value(file_item_byte, b'1'):
                counter += 1
        return counter

    def local_verificator2(self):
        # Executed only once
        verification = self.db_backup.get_value(
            self.mark_of_local_verification)
        if verification is not None:
            return
        start_time = self.utils.get_time_it()
        for file_item in self.utils.get_all_files(self.volume_dir + '/**'):
            if file_item == self.volume_dir + '/':
                continue
            file_item_byte = self.utils.encode_str_to_byte(
                self.utils.get_base_name_from_file(file_item))
            # If not present, create it to future synch.
            if not self.db_backup.get_equal_value(file_item_byte, b'1'):
                self.db_backup.update_or_insert_value(file_item_byte, b'0')
        self.db_backup.update_or_insert_value(
            self.mark_of_local_verification, b'1')
        end_time = self.utils.get_time_it()
        print('Local verification completed in ', end_time - start_time, '(s)')

    def count_files(self):
        counter = 0
        for file_item in self.utils.get_all_files(self.volume_dir + '/**'):
            if file_item == self.volume_dir + '/':
                continue
            counter += 1
        return counter

    def restore(self):
        if not self.utils.dir_exists(self.volume_dir):
            print('Dir {} does not exist'.format(self.volume_dir))
            return
        total_files = self.count_files_synchronized()
        # Restoring chunk configure
        restored = 0
        with self.db_backup.get_cursor_iterator() as txn:
            for _, data in enumerate(txn.cursor().iternext(keys=True, values=True)):
                bkey = data[0]
                bval = data[1]
                if bval == b'1':
                    continue
                req = CoreRequest(
                    self.server_host, self.server_port, '/' + self.const.SKYNET + '/' + self.const.START_BK)
                req.set_type(ReqType.POST)
                # We have to send the key, volume and port.

                req.set_payload({
                    'key': bkey,
                    'volume': self.volume_host.decode() + ':' + self.volume_port,
                    'total': total_files
                })
                req.make_request()
                py_object = self.utils.json_to_py(req.response)
                if 'msg' in py_object['response'] and py_object['response']['msg'] == 'ok':
                    # Mark as restored
                    self.db_backup.update_or_insert_value(
                        bkey,
                        b'1'
                    )
                    print('Record restored')
                    restored += 1
                if restored >= self.backup_chunk:
                    break

    def synchronize(self):
        # Gets disk usage
        percent = self.utils.giga_free_space()
        # Gets load usage
        volume_load = str(self.utils.cpu_info()[2])
        if self.volume_host is None or self.volume_port is None or self.restored_ready is None:
            print('No records created, auto-discovering')
            # Create backup DB once
            self.create_restore_DB()
            req = CoreRequest(
                '127.0.0.1',
                self.volume_port,
                '/autodiscovery'
            )
            req.make_request()
            print('response: ', req.response)
            return
        req = CoreRequest(
            self.server_host,
            self.server_port,
            self.const.SYNC
        )
        req.set_type(ReqType.POST)
        req.set_payload({
            'percent': percent,
            'load': volume_load,
            'host': self.volume_host.decode(),
            'port': self.volume_port,
            'total': self.count_files_synchronized()
        })
        req.make_request()
        if req.response is None:
            return
        py_object = self.utils.json_to_py(req.response)
        response = py_object['response']
        key_to_restore = self.db_backup.get_key_equal_to_value(b'0')
        if ('synch' in response and not response['synch'] or key_to_restore is not None):
            self.restore()


SYNCHRO = Synchro()
SYNCHRO.synchronize()
