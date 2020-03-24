import re
import shutil
from urllib.parse import urlparse

# Internal
from utils.constants import Constants

class Utils:
    def __init__(self):
        self.const = Constants()

    # Encode/decode section
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
            self.const.SERVER_PROTOCOL: env[self.const.SERVER_PROTOCOL]
        }

        return result