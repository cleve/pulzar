import requests
from enum import Enum

from utils.utils import Utils

class ReqType(Enum):
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4

class CoreRequest:
    def __init__(self, host, port, url_path):
        self.utils = Utils()
        self.host = host
        self.port = port
        self.path = url_path
        self.request_type = ReqType.GET
        self.payload = None

    def set_type(self, type_request='GET'):
        if type_request == 'GET':
            self.request_type = ReqType.GET
        elif type_request == 'POST':
            self.request_type = ReqType.POST
        elif type_request == 'PUT':
            self.request_type = ReqType.PUT
        elif type_request == 'DELETE':
            self.request_type = ReqType.DELETE

    def set_path(self, path_string):
        self.path = path_string

    def set_payload(self, payload):
        self.payload = payload

    def make_request(self):
        # Check
        req = None
        complete_url = 'http://' + self.host + ':' + self.port + self.path
        if self.request_type is None or self.path is None and self.utils.validate_url(complete_url):
            return False
        url_port = complete_url
        print('url_port: ', url_port)
        if self.request_type == ReqType.GET:
            req = requests.get(
                url_port,
                timeout=10
            )
        if self.request_type == ReqType.POST:
            print(':::::::::::::::::::::: calling POST ::::::::::::::::::::::')
            print (self.payload)
            req = requests.post(
                url_port,
                data=self.payload,
                timeout=10
            )
        
        if req.status_code == 200:
            return True
        return False

