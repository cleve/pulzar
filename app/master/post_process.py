from utils.utils import Utils
from core.core_db import DB


class PostProcess:
    def __init__(self, constants):
        self.const = constants
        self.utils = Utils()
        # DB of values already loaded
        self.db_values = DB(self.const.DB_PATH)
        self.db_volumes = DB(self.const.DB_VOLUME)

    def process_request(self, env, start_response, url_path):
