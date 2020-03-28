from core.core_request import CoreRequest
from utils.utils import Utils
from utils.constants import Constants
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
    # Gets disk usage
    percent = utils.giga_free_space()
    volume_host = db_stats.get_value(utils.encode_str_to_byte(const.SERVER_NAME))
    volume_port = db_stats.get_value(utils.encode_str_to_byte(const.SERVER_PORT))
    req = CoreRequest(
        server_host,
        server_port,
        const.SYNC
    )
    req.set_type('POST')
    req.set_payload({
        'percent': percent,
        'host': volume_host.decode(),
        'port': volume_port.decode()
        })
    req.make_request()
synchronize()