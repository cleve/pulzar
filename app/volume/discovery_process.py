from pulzarutils.utils import Utils
from pulzarcore.core_db import DB


class DiscoveryProcess:
    def __init__(self, constants):
        self.const = constants
        self.utils = Utils()

    def save_status(self, env):
        """Save stats to synch
        """
        db = DB(self.const.DB_STATS)
        result = db.update_or_insert_value(
            self.utils.encode_str_to_byte(self.const.HOST_NAME),
            self.utils.encode_str_to_byte(
                env[self.const.SERVER_NAME])
        )
        result = db.update_or_insert_value(
            self.utils.encode_str_to_byte(self.const.SERVER_PORT),
            self.utils.encode_str_to_byte(
                env[self.const.SERVER_PORT])
        )
        print(result)

    def process_request(self, env):
        """Just getting the data
        """
        try:
            self.save_status(env)
            return self.const.AUTODISCOVERY

        except Exception as err:
            print('Error::Autodiscovery', err)
