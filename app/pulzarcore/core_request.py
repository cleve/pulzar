import requests
from pulzarutils.constants import ReqType
from pulzarutils.utils import Utils


class CoreRequest:
    """Manage the requests
    """

    def __init__(self, host, port, url_path):
        self.utils = Utils()
        self.host = host
        self.port = port
        self.path = url_path
        self.request_type = ReqType.GET
        self.payload = None
        self.response = None
        self.json_response = None
        self.headers = {'user-agent': 'pulzar/1.0.3'}

    def add_header(self, header):
        '''Add headers to the request
        
        Parameters
        ----------
        header (dict): Dictionary with the headers

        Return
        ------
        None
        '''
        keys = header.keys()
        for key in keys:
            if key not in self.headers:
                self.headers[key] = header[key]

    def set_type(self, type_request=ReqType.GET):
        self.request_type = type_request

    def set_path(self, path_string):
        self.path = path_string

    def set_payload(self, payload):
        self.payload = payload

    def make_request(self, json_request=False):
        try:
            # Check
            req = None
            complete_url = 'http://' + self.host + ':' + self.port + self.path
            if self.request_type is None or self.path is None and self.utils.validate_url(complete_url):
                return False
            url_port = complete_url
            if self.request_type == ReqType.GET:
                req = requests.get(
                    url_port,
                    timeout=10
                )
            if self.request_type == ReqType.POST:
                if json_request:
                    req = requests.post(
                        url_port,
                        json=self.payload,
                        headers=self.headers,
                        timeout=10
                    )
                else:
                    req = requests.post(
                        url_port,
                        data=self.payload,
                        headers=self.headers,
                        timeout=10
                    )

            if req.status_code == 200:
                self.response = req.text
                if json_request:
                    self.json_response = req.json()
                return True
            self.response = req.text
            return False
        except Exception as err:
            print(err)
            self.response = 'no response'
            return False
