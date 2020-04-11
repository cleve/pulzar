from enum import Enum


class Response(Enum):
    JSON = 0
    TEXT = 1


class ReqType(Enum):
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4


class Constants:
    def __init__(self):
        # General
        self.DEBUG = True
        self.VERSION = '0.1'
        self.PASS = 'admin'
        self.PASSPORT = 'passport'

        # Config
        self.CONF_HOST = 'host'
        self.CONF_PORT = 'port'
        self.CONF_PATH = 'config/server.conf'

        # Database
        self.DB_PATH = 'storage/master.db'
        self.DB_VOLUME = 'storage/volume.db'
        self.DB_STATS = 'storage/volume_st.db'

        # Env
        self.REQUEST_METHOD = 'REQUEST_METHOD'
        self.SERVER_NAME = 'SERVER_NAME'
        self.SERVER_PORT = 'SERVER_PORT'
        self.PATH_INFO = 'PATH_INFO'
        self.QUERY_STRING = 'QUERY_STRING'
        self.HTTP_USER_AGENT = 'HTTP_USER_AGENT'
        self.SERVER_PROTOCOL = 'SERVER_PROTOCOL'
        self.CONTENT_LENGTH = 'CONTENT_LENGTH'
        self.WSGI_INPUT = 'wsgi.input'

        self.POST = 'POST'
        self.GET = 'GET'

        # REST admin paths
        self.SKYNET = '/skynet'
        self.REGISTER = self.SKYNET + '/register'
        self.SYNC = self.SKYNET + '/sync'

        # REGEX
        self.RE_URL_LAST = r'([^/]+$)'
        self.RE_URL_OPTION_ORDER = r'([\w]+)*\/([\w]+)+$'

        # API calls
        self.RE_GET_VALUE = r'/get_key/(\w+)$'
        self.RE_POST_VALUE = r'/add_key/(\w+)$'

        # Type of requests
        self.REGULAR_GET = 'regular'
        self.REGULAR_PUT = 'put'
        self.ADMIN = 'admin'
        self.SKYNET = 'skynet'
        self.KEY_NOT_FOUND = 'key_not_found'
