from pulzarutils.utils import Utils
from pulzarcore.core_db import DB
from pulzarcore.core_rdb import RDB


class NodeUtils:
    """Node helper
    """

    def __init__(self, constants):
        self.const = constants
        # 20 mins max to consider a volume online.
        self.second_range = 1200
        self.utils = Utils()
        # DB of volumes/keys.
        self.db_volumes = DB(self.const.DB_VOLUME)
        # Jobs database
        self.job_db = RDB(self.const.DB_JOBS)

    def discover_volume(self):
        """Get the volume name

        return: (str)
        """
        keys = self.db_volumes.get_keys()
        if keys is None:
            return None
        return keys[0].decode()

    def pick_a_volume(self):
        """Volume selection using the load
            return (byte): URL without port
        """
        volumes = self.db_volumes.get_keys_values()
        current_datetime = self.utils.get_current_datetime()
        min_value = 100
        server = None
        for elem in volumes:
            # meta_raw[0] = percent, meta_raw[1] = load
            meta_raw = self.utils.decode_byte_to_str(elem[1]).split(':')
            percent = int(meta_raw[0])
            last_update_reported = self.utils.get_datetime_from_string(
                meta_raw[3])
            delta_time = current_datetime - last_update_reported
            # Check availability of node.
            if delta_time.total_seconds() >= self.second_range:
                continue
            if percent < min_value:
                min_value = percent
                server = elem[0]
        return server
