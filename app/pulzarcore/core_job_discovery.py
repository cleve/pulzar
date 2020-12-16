import os
import importlib
from pulzarutils.utils import Utils
from pulzarutils.constants import Constants
from pulzarutils.stream import Config
from pulzarcore.core_rdb import RDB


class JobDiscovery:
    """Discovery section

        This class inspect into the job directory
        in order to build a catalog. This catalog can 
        be used by the api/web interface
    """

    def __init__(self):
        self.TAG = self.__class__.__name__
        self.utils = Utils()
        self.const = Constants()
        self.rdb = RDB(self.const.DB_JOBS)
        server_config = Config(self.const.CONF_PATH)
        self.job_directory = server_config.get_config('jobs', 'dir')
        self._clean_repository()

    def _get_directories(self):
        """Only one level
        """
        with os.scandir(self.job_directory) as it:
            for entry in it:
                # Directories
                if not entry.name.startswith('.'):
                    complete_path = os.path.join(
                        self.job_directory, entry.name)
                    if not self.utils.dir_exists(complete_path):
                        continue
                    with os.scandir(complete_path) as file_it:
                        for file_entry in file_it:
                            # Avoid package file
                            if file_entry.name.find('__init__.py') >= 0:
                                continue
                            # Directories
                            if file_entry.name.endswith('.py') and file_entry.is_file():
                                url_path = os.path.join(
                                    entry.name, file_entry.name)
                                self._get_entrance_point(url_path)

    def _get_entrance_point(self, url_path):
        """Get the main app and extract
        documentation
        """
        no_extension = os.path.splitext(url_path)[0]
        class_name = no_extension.split('/')[1].capitalize()
        relative_path = os.path.join(self.job_directory, no_extension)
        to_module_notation = relative_path.replace('/', '.')
        try:
            import_fly = importlib.import_module(to_module_notation)
            job_class = getattr(import_fly, class_name)
            job_object = job_class({'job_id': '-1', '_pulzar_config': 'na'})
            dictionary = self._parse_doc(job_object.execute.__doc__)

            # Storing results
            self._create_or_update_catalog(no_extension, dictionary)
        except BaseException as err:
            print('{}::{}'.format(self.TAG, err))

    def _parse_doc(self, raw_text):
        config = {
            'description': '',
            'arguments': '',
            'category': '',
            'author': ''
        }
        raw_list = filter(lambda x: x != '',
                          raw_text.split('\n'))

        for item in raw_list:
            strip_item = item.strip()
            if strip_item.upper().find('DESCRIPTION') == 0 and strip_item.find(':') >= 0:
                config['description'] = strip_item.split(':', 1)[1].strip()
            elif strip_item.upper().find('ARGUMENTS') == 0 and strip_item.find(':') >= 0:
                config['arguments'] = strip_item.split(':', 1)[1].strip()
            elif strip_item.upper().find('CATEGORY') == 0 and strip_item.find(':') >= 0:
                config['category'] = strip_item.split(
                    ':', 1)[1].strip().upper()
            elif strip_item.upper().find('AUTHOR') == 0 and strip_item.find(':') >= 0:
                config['author'] = strip_item.split(':', 1)[1].strip()

        return config

    def _clean_repository(self):
        """Clean catalog
        """
        sql = 'DELETE FROM job_catalog'
        self.rdb.execute_sql(sql)

    def _create_or_update_catalog(self, job_path, dictionary):
        """To DB
        """
        query = """
            INSERT INTO job_catalog(path, description, args, category, author)
                VALUES(?, ?, ?, ?, ?) 
                ON CONFLICT(path) DO UPDATE SET description=?, args=?, category=?, author=?;
        """
        rows_affected = self.rdb.execute_sql_insert(
            query, (
                job_path,
                dictionary['description'],
                dictionary['arguments'],
                dictionary['category'],
                dictionary['author'],
                dictionary['description'],
                dictionary['arguments'],
                dictionary['category'],
                dictionary['author'],
            )
        )

    def discover(self):
        """Start the catalog process
        """
        self._get_directories()
