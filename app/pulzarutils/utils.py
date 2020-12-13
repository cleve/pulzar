import re
import random
import string
import shutil
import json
import base64
import tempfile
from urllib.parse import urlparse
import glob
import os
import platform
import datetime
import time
from timeit import default_timer as timer
from urllib.parse import urlsplit
from urllib.parse import parse_qs
import psutil
import requests

# Internal
from pulzarutils.constants import Constants


class Utils:
    """Utilities for vari
    """

    def __init__(self):
        self.const = Constants()

    # System
    def is_unix(self):
        """Getting True or False for
        plattform
        """
        return platform.system() == 'Linux'

    def get_random_string(self, n):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))

    # Datetime options
    def get_current_datetime_utc(self, to_string=False, db_format=True):
        """Get datetime in UTC
        """
        datetime_object = datetime.datetime.now(tz=datetime.timezone.utc)
        if to_string:
            return self.datetime_to_string(datetime_object, db_format)
        return datetime_object

    def get_current_datetime_str(self, db_format=False):
        if db_format:
            return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S%z")
        return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    def datetime_to_utc_string(self, datetime_object, db_format=False):
        utc_dt = datetime.datetime.fromtimestamp(
            datetime_object.timestamp(), tz=datetime.timezone.utc)
        return self.datetime_to_string(utc_dt, db_format)

    def datetime_to_utc(self, datetime_object, db_format=False):
        utc_dt = datetime.datetime.fromtimestamp(
            datetime_object.timestamp(), tz=datetime.timezone.utc)
        return utc_dt

    def datetime_to_string(self, datetime_object, db_format=False):
        if db_format:
            return datetime_object.strftime("%Y-%m-%d %H:%M:%S%z")
        return datetime_object.strftime("%Y-%m-%d-%H-%M-%S")

    def get_current_datetime(self):
        return datetime.datetime.now()

    def get_date_days_diff(self, days, to_string=False):
        """Get days difference using the current date as base
        :param days: amount of days to operate
        :type days: int
        :return: date operated
        :rtype: date or string
        """
        date_object = datetime.date.today() + datetime.timedelta(days=days)
        if to_string:
            return date_object.strftime('%Y-%m-%d')
        return date_object

    def get_date_today(self, to_string=False):
        """Get the curren date
        :param to_string: Boolean to get string or object
        :return: current date
        :rtype: date or string
        """
        date_object = datetime.date.today()
        if to_string:
            return date_object.strftime('%Y-%m-%d')
        return date_object

    def get_datetime_from_string(self, datetime_str, full=False):
        if full:
            return datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f")
        return datetime.datetime.strptime(datetime_str, "%Y-%m-%d-%H-%M-%S")

    def get_standard_datetime_from_string(self, datetime_str, full=False, data_base=False):
        if full:
            if data_base:
                return datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S%z")
            return datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f")
        return datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

    def get_time_it(self):
        return timer()

    # JSON section
    def py_to_json(self, py_object, to_bin=False):
        return json.dumps(py_object) if not to_bin else self.encode_str_to_byte(json.dumps(py_object))

    def json_to_py(self, json_srt):
        """JSON to python object
        """
        return json.loads(json_srt)

    # Encode/decode section
    def encode_base_64(self, string, to_str=False) -> bytes or str:
        '''Encode base64

        Parameters
        ----------
        sting : str
            string to be encoded
        to_str : bool, default=False
            If the parameter is True, the return will be str
        Return
        ------
        str or binary string
        '''
        byte_string = self.encode_str_to_byte(string)
        return base64.b64encode(byte_string) if not to_str else self.decode_byte_to_str(base64.b64encode(byte_string))

    def encode_byte_base_64(self, bstring, to_str=False):
        byte_string = bstring
        return base64.b64encode(byte_string) if not to_str else self.decode_byte_to_str(base64.b64encode(byte_string))

    def decode_base_64(self, string64, to_str=False):
        return base64.b64decode(string64) if not to_str else self.decode_byte_to_str(base64.b64decode(string64))

    def decode_string_base_64(self, string, to_str=False) -> bytes or str:
        '''Decode stringB64 to str

        Paramater
        ---------
        string : str
            string to be decoded
        to_str : bool
            if its True return string decoded string
        
        Return
        ------
        str or byte string : str or byte
            Dependent of the to_str parameter
        '''
        return base64.b64decode(string.encode()) if not to_str else self.decode_byte_to_str(base64.b64decode(string.encode()))

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

    def cpu_info(self):
        """Get list of load:
            [last 1 minute avg, last 5 minutes avg, last 15 minutes avg]
        """
        cpus = psutil.cpu_count()
        return [x / cpus * 100 for x in psutil.getloadavg()]

    # REGEX section
    def make_regex(self, string):
        """Just compile the string into regex
        """
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
            file_list_raw = glob.glob(os.path.join(os.getcwd(), dir_path, '*'))
        file_list_raw = glob.glob(os.path.join(
            os.getcwd(), dir_path, '*.' + file_type))
        for raw_path in file_list_raw:
            file_list.append(os.path.basename(raw_path))
        return file_list

    def get_sub_directories(self, dir_path):
        return os.scandir(dir_path)

    def get_base_name_from_file(self, path_name):
        """Get file name only
        """
        return os.path.basename(path_name)

    def get_parent_name_from_file(self, path_name):
        """Get all parents of a given path
        """
        return os.path.dirname(path_name)

    def get_all_files(self, directory, rec=True):
        """Return an iterator
            directory must have /.../** in order to get recursive results
        """
        return glob.iglob(directory, recursive=rec)

    def file_exists(self, file_path):
        """Just a binding
        """
        return os.path.isfile(file_path)

    def remove_file(self, file_path):
        """Remove file if exists
        """
        if self.file_exists(file_path):
            os.remove(file_path)
            return True
        print('File {} does not exist'.format(file_path))

    def dir_exists(self, dir_path):
        """Just a binding
        """
        return os.path.isdir(dir_path)

    def remove_dir(self, dir_path):
        """Remove dir if exists
        """
        if self.dir_exists(dir_path):
            return os.rmdir(dir_path)

    def get_absolute_path_of_dir(self):
        """Get the absolute path of the
        current location
        """
        return os.path.abspath(os.getcwd())

    def join_path(self, base_path, child_path):
        """Just a binding
        """
        return os.path.join(base_path, child_path)

    # Custom methods
    def extract_query_params(self, complete_url):
        query = urlsplit(complete_url).query
        params = parse_qs(query)
        return params

    def extract_url_data(self, complete_url):
        data = {
            'host': None,
            'port': None,
        }
        split_data = complete_url.split(':')
        if len(split_data) == 2:
            data['host'] = split_data[0]
            data['port'] = split_data[1]
        return data

    def bytesto(self, bytes, to, bsize=1024):
        '''Convert units
        '''
        a = {'k': 1, 'm': 2, 'g': 3, 't': 4, 'p': 5, 'e': 6}
        r = float(bytes)
        return bytes / (bsize ** a[to])

    @staticmethod
    def download_file(url):
        '''Download file from http
        '''
        try:
            temporary_file = tempfile.NamedTemporaryFile(delete=False)
            # Open in binary mode
            with open(temporary_file.name, 'wb') as file:
                response = requests.get(url, stream=True, timeout=20)
                if response.status_code >= 400:
                    raise Exception('The server response has errors')
                file.write(response.content)
            return temporary_file
        except Exception as err:
            print(err)
            return None
