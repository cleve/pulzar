from core.core_request import CoreRequest
from utils.utils import Utils
from utils.constants import Constants
from core.core_db import DB
from utils.stream import Config
import shutil

def synchronize():
    utils = Utils()
    const = Constants()
    config = Config(const.CONF_PATH)
    db = DB(const.DB_STATS)
    # Gets disk usage
    percent = utils.giga_free_space()
    host = db.get_value(utils.encode_str_to_byte(const.SERVER_NAME))
    port = db.get_value(utils.encode_str_to_byte(const.SERVER_PORT))
    req = CoreRequest(
        host,
        port,
        const.SYNC
    )
    req.set_payload({'percent': percent})
synchronize()