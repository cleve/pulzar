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
        self.dir_path = 'jobs'

    def _get_directories(self):
        """Only one level
        """
        with os.scandir(self.dir_path) as it:
            for entry in it:
                # Directories
                if not entry.name.startswith('.'):
                    complete_path = os.path.join(self.dir_path, entry.name)
                    with os.scandir(complete_path) as file_it:
                        for file_entry in file_it:
                            # Directories
                            if file_entry.name.endswith('.py') and file_entry.is_file():
                                print(complete_path)
                                print(file_entry.name)

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
        self._get_directories()
