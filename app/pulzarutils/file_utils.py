from pulzarutils.utils import Utils
from pulzarutils.utils import Constants
from pulzarutils.stream import Config
import os


class FileUtils():
    def __init__(self):
        self.utils = Utils()
        self.config = Config(Constants.CONF_PATH)
        self.binary_key = b''
        self.key = ''
        self.base_dir = None
        self.volume_path = ''
        # Max size allowed to store
        self.max_size = 1000
        self.init_config()

    def init_config(self):
        if Constants.DEBUG:
            directory = os.path.join(
                self.utils.get_absolute_path_of_dir(),
                Constants.DEV_DIRECTORY
            )
        else:
            directory = self.config.get_config('volume', 'dir')
        self.max_size = int(self.config.get_config('general', 'maxsize'))
        self.volume_path = directory

    def set_key(self, binary_key, base64_str_key):
        self.binary_key = binary_key
        self.key = base64_str_key

    def set_path(self, root_path):
        """Defining the basedir
        """
        self.base_dir = root_path

    def get_key(self):
        return self.key

    def get_decoded_key(self):
        """Get the complete path
        return (str)
        """
        return self.utils.decode_base_64(self.key, to_str=True)

    def is_value_present(self, key_name):
        value_path = self.volume_path + '/' + key_name
        return self.file_exists(value_path)

    def file_exists(self, file_path):
        return os.path.isfile(file_path)

    def dir_exists(self, dir_path):
        return os.path.isdir(dir_path)

    def remove_file_with_path(self, full_path):
        file_path = self.utils.join_path(self.volume_path, full_path)
        if self.file_exists(file_path):
            os.remove(file_path)
            return True
        return False

    def remove_file(self):
        """If error delete file
        """
        file_path = self.utils.join_path(self.volume_path, self.key)
        if self.file_exists(file_path):
            os.remove(file_path)
            return True
        return False

    def read_value(self, key_name, start_response):
        value_path = self.utils.join_path(self.volume_path, key_name)
        if not self.utils.file_exists(value_path):
            raise Exception(f'{self.__class__.__name__}::file {value_path} does not exists')
        fh = open(value_path, 'rb')
        start_response(
            '200 OK', [('Content-Type', 'application/octet-stream')])
        return self.fbuffer(fh, 1024)

    def fbuffer(self, f, chunk_size):
        '''Generator to buffer file chunks'''
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

    def read_binary_local_file(self, file_path):
        """Storing file created locally
        """
        destiny_path = self.utils.join_path(self.volume_path, self.key)
        temp_file = self.utils.get_tmp_file()
        # Read binary file
        with open(file_path, 'rb') as f:
            for piece in self.read_in_chunks(f):
                temp_file.write(piece)

        # Creating directories if does not exist.
        full_path = self.volume_path + self.base_dir
        if self.base_dir is not None and not self.utils.dir_exists(full_path):
            os.makedirs(full_path)

        temp_file.close()  # Close the file to be copied.
        if destiny_path == self.utils.move_file(
                temp_file.name, self.utils.join_path(full_path, self.key)):
            return self.key

    def read_binary_file(self, env) -> str:
        '''Read the file sent by client

        Parameters
        ----------
        env : dict
            Uwsgi environment dictionary

        Return
        ------
        str : Base64 string
        '''
        try:
            request_body_size = int(env[Constants.CONTENT_LENGTH])
        except (ValueError):
            request_body_size = 0
        if request_body_size > 0:
            # Checking max size
            to_mb = self.utils.bytesto(request_body_size, 'm')
            if to_mb > self.max_size:
                raise Exception(
                    'max size allowed is {}MB'.format(self.max_size))
            temp_file = self.utils.get_tmp_file()
            # Read binary file sent.
            f = env[Constants.WSGI_INPUT]
            for piece in self.read_in_chunks(f):
                temp_file.write(piece)

            # Creating directories if does not exist.
            full_path = self.volume_path + self.base_dir
            if self.base_dir is not None and not self.utils.dir_exists(full_path):
                os.makedirs(full_path)

            temp_file.close()  # Close the file to be copied.
            self.utils.move_file(
                temp_file.name,
                self.utils.join_path(full_path, self.key)
            )
            return self.key

    def read_in_chunks(self, file_object, chunk_size=1024):
        """Lazy function (generator) to read a file piece by piece.
        Default chunk size: 1k."""
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data
