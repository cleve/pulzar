import re

class Utils:
    def __init__(self):
        pass

    # REGEX section
    def make_regex(self, string):
        return re.compile(string)

    def match_regex(self, string, regex_str):
        """True or False"""
        obj_result = self.make_regex(regex_str).match(string)
        return True if obj_result else False