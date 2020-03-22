import requests

class CoreRequest:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.type = None
        self.path = None

    def set_type(self, type_request='GET'):
        pass

    def set_path(self, path_string):
        pass

    def make_request(self):
        # Check
        if self.type is None or self.path is None:
            return None

