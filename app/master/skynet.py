from core.core_db import DB
from utils.constants import Constants
from utils.utils import Utils

class Skynet:
    def __init__(self):
        self.const = Constants()
        self.utils = Utils()
        self.db_volume = DB(self.const.DB_VOLUME)

        # Skynet options
        self.sync_status = self.const.SKYNET + '/sync/'

    def sync_volume(self, volume_name, space):
        self.db_volume.update_or_insert_value(
            self.utils.encode_str_to_byte(volume_name),
            self.utils.encode_str_to_byte(space)
        )

    def process_request(self, url_path):
        if url_path.find(self.sync_status) == 1:
            # Extracting last section of the url
            groups = self.utils.get_search_regex(
                url_path,
                self.const.RE_URL_OPTION_ORDER
            )
            if groups:
                volume, percent = groups.groups()
                self.sync_volume(volume, percent)

