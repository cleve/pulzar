from utils.utils import Utils
from utils.stream import Config
import os


class FileUtils():
    def __init__(self, const):
        self.const = const
        self.utils = Utils()
        self.config = Config(self.const.CONF_PATH)
        self.binary_key = b''
        self.key = ''
        self.volume_path = ''
        self.init_config()

    def init_config(self):
        directory = self.config.get_config('volume', 'dir')
        self.volume_path = directory

    def set_key(self, binary_key, base64_str_key):
        self.binary_key = binary_key
        self.key = base64_str_key

    def file_exists(self, file_path):
        return os.path.isfile(file_path)

    def dir_exists(self, dir_path):
        return os.path.isdir(dir_path)

    def read_binary_file(self, env):
        try:
            request_body_size = int(env[self.const.CONTENT_LENGTH])
        except (ValueError):
            request_body_size = 0
        if request_body_size > 0:
            destiny_path = self.volume_path + '/' + self.key
            temp_file = self.utils.get_tmp_file()
            # Read binary file sent.
            f = env[self.const.WSGI_INPUT]
            for piece in self.read_in_chunks(f):
                temp_file.write(piece)
            if destiny_path == self.utils.move_file(
                    temp_file.name, self.volume_path + '/' + self.key):
                temp_file.close()
                return self.key

    def read_in_chunks(self, file_object, chunk_size=1024):
        """Lazy function (generator) to read a file piece by piece.
        Default chunk size: 1k."""
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data
