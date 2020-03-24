import re
import shutil

class Utils:
    def __init__(self):
        pass

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