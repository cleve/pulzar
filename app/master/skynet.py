from core.core_db import DB
from utils.constants import Constants
from utils.utils import Utils
from core.core_body import Body

class Skynet:
    def __init__(self, env):
        self.const = Constants()
        self.utils = Utils()
        self.env = env
        self.db_volume = DB(self.const.DB_VOLUME)

        # Skynet options
        self.sync_status = self.const.SKYNET + '/sync'

    def sync_volume(self):
        body = Body()
        params = body.extract_params(self.env)
        self.db_volume.update_or_insert_value(
            params[b'host'][0],
            params[b'percent'][0]
        )

    def process_request(self, url_path, method):
        if method != self.const.POST:
            return None
        if url_path.find(self.sync_status) == 1:
            # Extracting last section of the url
            groups = self.utils.get_search_regex(
                url_path,
                self.const.RE_URL_OPTION_ORDER
            )
            if groups is None:
                return None
            
            self.sync_volume()

