import re
import shutil
import json
import base64
import tempfile
from urllib.parse import urlparse
import glob
import os

# Internal
from utils.constants import Constants


class Utils:
    def __init__(self):
        self.const = Constants()

    # JSON section
    def py_to_json(self, py_object, to_bin=False):
        return json.dumps(py_object) if not to_bin else self.encode_str_to_byte(json.dumps(py_object))

    def json_to_py(self, json_srt):
        return json.loads(json_srt)

    # Encode/decode section
    def encode_base_64(self, string, to_str=False):
        byte_string = self.encode_str_to_byte(string)
        return base64.b64encode(byte_string) if not to_str else self.decode_byte_to_str(base64.b64encode(byte_string))

    def encode_str_to_byte(self, string):
        return string.encode()

    def decode_byte_to_str(self, b_string):
        return b_string.decode('ascii')

    # System info section
    def giga_free_space(self):
        """Used disk information in %
        return: str
        """
        disk_usage = shutil.disk_usage("/")
        return str(int((disk_usage.used / disk_usage.total) * 100))

    # REGEX section
    def make_regex(self, string):
        return re.compile(string)

    def match_regex(self, string, regex_str):
        """True or False"""
        obj_result = self.make_regex(regex_str).match(string)
        return True if obj_result else False

    def get_search_regex(self, string, regex_str):
        """Return regex object"""
        obj_result = self.make_regex(regex_str).search(string)
        if obj_result:
            return obj_result
        return None

    # URL section
    def validate_url(self, url_string):
        try:
            result = urlparse(url_string)
            return all([result.scheme, result.netloc, result.path])
        except:
            return False

    # Environmet vars section
    def extract_host_env(self, env):
        """Return dictionary with env elements"""
        result = {
            self.const.SERVER_NAME: env[self.const.SERVER_NAME],
            self.const.REQUEST_METHOD: env[self.const.REQUEST_METHOD],
            self.const.SERVER_PORT: env[self.const.SERVER_PORT],
            self.const.PATH_INFO: env[self.const.PATH_INFO],
            self.const.QUERY_STRING: env[self.const.QUERY_STRING],
            self.const.HTTP_USER_AGENT: env[self.const.HTTP_USER_AGENT],
            self.const.SERVER_PROTOCOL: env[self.const.SERVER_PROTOCOL],
            self.const.HTTP_HOST: env[self.const.HTTP_HOST]
        }

        return result

    # Temporary section
    def get_tmp_file(self):
        """Dont forget to close the file
        """
        return tempfile.NamedTemporaryFile(delete=False)

    # File operations
    def move_file(self, source, dest):
        return shutil.copy2(source, dest)

    # Read files from dir
    def read_file_name_from_dir(self, dir_path, file_type=None):
        file_list = []
        if file_type is None:
            file_list_raw = glob.glob(os.getcwd() + dir_path + '*')
        file_list_raw = glob.glob(os.getcwd() + dir_path + '*.' + file_type)
        for raw_path in file_list_raw:
            file_list.append(os.path.basename(raw_path))
        return file_list

    # Custom methods
    def extract_url_data(self, complete_url):
        data = {
            'host': None,
            'port': None
        }
        if complete_url.find(':') == -1 or complete_url.find('=') == -1:
            return data
        split_query = complete_url.split('=')[1]
        split_data = split_query.split(':')
        if len(split_data) == 2:
            data['host'] = split_data[0]
            data['port'] = split_data[1]
        return data
