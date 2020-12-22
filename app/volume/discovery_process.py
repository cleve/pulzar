from pulzarutils.utils import Utils
from pulzarutils.messenger import Messenger
from pulzarcore.core_db import DB


class DiscoveryProcess:
    def __init__(self, constants, logger):
        self.TAG = self.__class__.__name__
        self.const = constants
        self.logger = logger
        self.utils = Utils()
        self.messenger = Messenger()

    def _save_status(self, env):
        """Save stats to synch
        
        Parameters
        ----------
        env : dict
            uWsgi enviroment
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

    def process_request(self, env):
        """Just getting the data
        """
        try:
            self._save_status(env)
            self.messenger.code_type = self.const.AUTODISCOVERY
            self.messenger.set_message = 'ok'

        except Exception as err:
            self.logger.exception('{}:{}'.format(self.TAG, err))
            self.messenger.code_type = self.const.PULZAR_ERROR
            self.messenger.set_message = str(err)
            self.messenger.mark_as_failed()

        return self.messenger
