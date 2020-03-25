from core.core_request import CoreRequest
from utils.utils import Utils
from utils.constants import Constants
from core.core_db import DB
import shutil

def synchronize():
    utils = Utils()
    const = Constants()
    db = DB(const.DB_STATS)
    # Gets disk usage
    percent = utils.giga_free_space()
    print('Percent: ', percent)
    host = db.get_value(utils.encode_str_to_byte(const.SERVER_NAME))
    print('HOST ===> ', host)

synchronize()