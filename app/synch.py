from core.core_request import CoreRequest
from utils.utils import Utils
from utils.constants import Constants
from utils.constants import ReqType
from core.core_db import DB
from utils.stream import Config
import shutil


def synchronize():
    utils = Utils()
    const = Constants()
    server_config = Config(const.CONF_PATH)
    db_stats = DB(const.DB_STATS)
    server_host = server_config.get_config('server', 'host')
    server_port = server_config.get_config('server', 'port')
    # Volume machine
    volume_port = server_config.get_config('volume', 'port')
    # Gets load usage
    volume_load = str(utils.cpu_info()[3])
    # Gets disk usage
    percent = utils.giga_free_space()
    volume_host = db_stats.get_value(
        utils.encode_str_to_byte(const.SERVER_NAME))
    
    if volume_host is None or volume_port is None:
        print('No records created, auto-discovering')
        req = CoreRequest(
            '127.0.0.1',
            volume_port,
            '/autodiscovery'
        )
        req.make_request()
        return
    req = CoreRequest(
        server_host,
        server_port,
        const.SYNC
    )
    req.set_type(ReqType.POST)
    req.set_payload({
        'percent': percent,
        'load': volume_load,
        'host': volume_host.decode(),
        'port': volume_port
    })
    req.make_request()


synchronize()
