from pulzarcore.core_request import CoreRequest
from pulzarutils.utils import Utils
from pulzarutils.constants import Constants
from pulzarutils.constants import ReqType
from pulzarutils.logger import PulzarLogger
from pulzarcore.core_db import DB
from pulzarcore.core_rdb import RDB
from pulzarutils.stream import Config


class Synchro:
    """Check synchro between volume and master
    """

    def __init__(self):
        self.TAG = self.__class__.__name__
        self.const = Constants()
        self.logger = PulzarLogger(self.const, master=False)
        self.utils = Utils()
        self.db_stats = DB(self.const.DB_STATS)
        self.db_backup = DB(self.const.DB_BACKUP)
        self.rdb = RDB(self.const.DB_NODE_JOBS)
        self.key = None
        self.volume_host = None
        self.server_host = None
        self.server_port = None
        self.volume_port = None
        self.backup_chunk = None
        self.mark_of_local_verification = b'varidb_execute_file_verification'
        # Init main variables
        self.get_config()

    def get_config(self):
        """Configuration from ini file
        """
        server_config = Config(self.const.CONF_PATH)
        if self.const.DEBUG:
            self.volume_dir = self.const.DEV_DIRECTORY
        else:
            self.volume_dir = server_config.get_config('volume', 'dir')
        self.volume_host = self.db_stats.get_value(
            self.utils.encode_str_to_byte(self.const.HOST_NAME))
        self.volume_port = server_config.get_config('volume', 'port')
        self.key = server_config.get_config('server', 'key')
        # Master url
        self.server_host = server_config.get_config('server', 'host')
        self.server_port = server_config.get_config('server', 'port')

    def create_restore_db(self):
        """Create backup DB with the filesystem
        """
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
        """Counting files using backup DB
        """
        counter = 0
        for file_item in self.utils.get_all_files(self.volume_dir + '/**'):
            if file_item == self.volume_dir + '/':
                continue
            file_item_byte = self.utils.encode_str_to_byte(
                self.utils.get_base_name_from_file(file_item))
            if self.db_backup.get_equal_value(file_item_byte, b'1'):
                counter += 1
        return counter

    def local_verificator(self):
        """Compare the filesystem with the data restored
        """
        start_time = self.utils.get_time_it()
        for file_item in self.utils.get_all_files(self.volume_dir + '/**'):
            if file_item == self.volume_dir + '/' or self.utils.dir_exists(file_item):
                continue
            file_item_byte = self.utils.encode_str_to_byte(
                self.utils.get_base_name_from_file(file_item))
            # If not present, create it to future synch.
            if not self.db_backup.get_equal_value(file_item_byte, b'1'):
                self.db_backup.update_or_insert_value(file_item_byte, b'0')
        end_time = self.utils.get_time_it()
        self.logger.info(':{}:Local verification completed in -> {}(s)'.format(self.TAG, end_time - start_time))

    def restore(self):
        """Start backup process
        """
        if not self.utils.dir_exists(self.volume_dir):
            self.logger.error(':{}:dir does not exist -> {}'.format(self.TAG, self.volume_dir))
            return
        self.local_verificator()
        total_files = self.count_files_synchronized()
        # Restoring
        with self.db_backup.get_cursor_iterator() as txn:
            # Prevent other instance of backup process.
            self.db_backup.update_or_insert_value(
                self.mark_of_local_verification,
                b'0'
            )
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
                req.add_header({
                    self.const.PASSPORT: self.utils.encode_base_64(self.key)
                })
                req.make_request()
                py_object = self.utils.json_to_py(req.response)
                if 'status' in py_object and py_object['status'] == 'ok':
                    # Mark as restored
                    self.db_backup.update_or_insert_value(
                        bkey,
                        b'1'
                    )
            self.db_backup.delete_database()
            self.logger.info('Restauration completed')

    def get_catalog(self) -> list:
        '''Get catalog of node

        Return
        ------
        dict
            List with dictionary containing path, args, type and author
        '''
        response = []
        query = 'SELECT path, description, args, author FROM job_catalog'
        result = self.rdb.execute_sql_with_results(query)
        for item in result:
            response.append({
                'path': item[0],
                'description': item[1],
                'args': item[2],
                'author': item[3],
            })
        
        return response
    
    def synchronize(self):
        """Check status and send data to master
        """
        # Gets disk usage
        percent = self.utils.giga_free_space()
        # Gets load usage
        volume_load = str(self.utils.cpu_info()[2])
        if self.volume_host is None or self.volume_port is None:
            print('No records created, auto-discovering')
            # Create backup DB once
            self.create_restore_db()
            req = CoreRequest(
                '127.0.0.1',
                self.volume_port,
                '/autodiscovery'
            )
            req.make_request()
            return
        # Get catalog information
        catalog = self.get_catalog()

        # Preparing request
        req = CoreRequest(
            self.server_host,
            self.server_port,
            self.const.SYNC
        )
        req.add_header({
                self.const.PASSPORT: self.utils.encode_base_64(self.key)
            })
        req.set_type(ReqType.POST)
        req.set_payload({
            'percent': percent,
            'load': volume_load,
            'host': self.volume_host.decode(),
            'port': self.volume_port,
            'total': self.count_files_synchronized(),
            'catalog': self.utils.py_to_json(catalog)
        })
        req.make_request()
        if req.response is None:
            return
        py_object = self.utils.json_to_py(req.response)
        response = py_object['data']
        # Check restore process.
        verification = self.db_backup.get_value(
            self.mark_of_local_verification)
        if verification is not None and verification == b'1':
            self.restore()


SYNCHRO = Synchro()
SYNCHRO.synchronize()
