from pulzarutils.utils import Utils
from pulzarutils.utils import Constants
from pulzarutils.messenger import Messenger
from pulzarcore.core_db import DB


class DiscoveryProcess:
    def __init__(self, logger):
        self.TAG = self.__class__.__name__
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
        db = DB(Constants.DB_STATS)
        result = db.update_or_insert_value(
            self.utils.encode_str_to_byte(Constants.HOST_NAME),
            self.utils.encode_str_to_byte(
                env[Constants.SERVER_NAME])
        )
        result = db.update_or_insert_value(
            self.utils.encode_str_to_byte(Constants.SERVER_PORT),
            self.utils.encode_str_to_byte(
                env[Constants.SERVER_PORT])
        )

    def process_request(self, env):
        """Just getting the data
        """
        try:
            self._save_status(env)
            self.messenger.code_type = Constants.AUTODISCOVERY
            self.messenger.set_message = 'ok'

        except Exception as err:
            self.logger.exception('{}:{}'.format(self.TAG, err))
            self.messenger.code_type = Constants.PULZAR_ERROR
            self.messenger.set_message = str(err)
            self.messenger.mark_as_failed()

        return self.messenger
