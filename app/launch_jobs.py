from utils.utils import Utils
from utils.constants import Constants
from core.core_rdb import RDB


class LaunchJobs:
    """Handle job scheduled
    """

    def __init__(self):
        self.const = Constants()
        self.utils = Utils()
        self.data_base = RDB(self.const.DB_NODE_JOBS)

    def search_jobs(self):
        """Search job scheduled
        """
        pass
