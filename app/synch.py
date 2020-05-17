from core.core_request import CoreRequest
from utils.utils import Utils
from utils.constants import Constants
from utils.constants import ReqType
from core.core_db import DB
from utils.stream import Config
import shutil
import os

class Synchro:
    def __init__(self, *args, **kwargs):
        self.const = Constants()
        self.utils = Utils()
        self.db_stats = DB(self.const.DB_STATS)
        self.volume_host = None
        self.server_host = None
        self.server_port = None
        self.volume_port = None
        # Init main variables
        self.get_config()

    def get_config(self):
        server_config = Config(self.const.CONF_PATH)
        self.volume_dir = server_config.get_config('volume', 'dir')
        self.volume_host = self.db_stats.get_value(
            self.utils.encode_str_to_byte(self.const.SERVER_NAME))
        self.volume_port = server_config.get_config('volume', 'port')
        # Master url
        self.server_host = server_config.get_config('server', 'host')
        self.server_port = server_config.get_config('server', 'port')

    def count_files(self):
        counter = 0
        for _ in self.utils.get_all_files(self.volume_dir + '/**'):
            counter += 1
        return counter - 1
    
    def restore(self):
        if not self.utils.dir_exists(self.volume_dir):
            print('Dir {} does not exist'.format(self.volume_dir))
            return
        total_files = self.count_files()
        # Confirming with master.
        req = CoreRequest(
            self.server_host, self.server_port, '/' + self.const.SKYNET + '/' + self.const.START_BK)
        req.set_type(ReqType.POST)
        # We have to send the key, volume and port.
        for file_item in self.utils.get_all_files(self.volume_dir + '/**'):
            if file_item == self.volume_dir + '/':
                continue
            print(file_item)
            req.set_payload({
                'key': self.utils.get_base_name_from_file(file_item),
                'volume': self.volume_host,
                'total': total_files
            })
            req.make_request()
            py_object = self.utils.json_to_py(req.response)
            if 'msg' in py_object['response'] and py_object['response']['msg'] == 'ok':
                print('Record added')
            

    def synchronize(self):
        # Gets disk usage
        percent = self.utils.giga_free_space()
        # Gets load usage
        volume_load = str(self.utils.cpu_info()[2])
        if self.volume_host is None or self.volume_port is None:
            print('No records created, auto-discovering')
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
            'total': self.count_files()
        })
        req.make_request()
        if req.response is None:
            return
        py_object = self.utils.json_to_py(req.response)
        response = py_object['response']
        if 'synch' in response and not response['synch']:
            self.restore()

synchro = Synchro()
synchro.synchronize()
