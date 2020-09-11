import os
from pulzarutils.utils import Utils


class JobDiscovery:
    """Discovery section

        This class inspect into the job directory
        in order to build a catalog. This catalog can 
        be used by the api/web interface
    """

    def __init__(self):
        self.utils = Utils()

    def _get_directories(self):
        """Only one level
        """
        pass

    def _get_entrance_point(self, directory):
        """Get the main app and extract
        documentation
        """
        pass

    def _create_or_update_catalog(self):
        """Search jobs
        """
        pass

    def discover(self):
        """Start the catalog process
        """
        pass
