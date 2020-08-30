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
        self.THIRD_PARTY_DIR = 'master/third_party'
        self.START_BK = 'start_backup'
        self.HOST_NAME = 'host'
        # DEV Directory to store data
        self.DEV_DIRECTORY = 'storage/data'

        # Config
        self.CONF_HOST = 'host'
        self.CONF_PORT = 'port'
        self.CONF_PATH = 'config/server.conf'

        # Databases
        self.DB_PATH = 'storage/master.db' if self.DEBUG else '/var/lib/pulzar/dbs/master.db'
        self.DB_VOLUME = 'storage/volume.db' if self.DEBUG else '/var/lib/pulzar/dbs/volume.db'
        self.DB_STATS = 'storage/volume_st.db' if self.DEBUG else '/var/lib/pulzar/dbs/volume_st.db'
        self.DB_BACKUP = 'storage/volume_bk.db' if self.DEBUG else '/var/lib/pulzar/dbs/volume_bk.db'
        self.DB_NOT_PERMANENT = 'storage/temporal_data.db' if self.DEBUG else '/var/lib/pulzar/dbs/temporal_data.db'
        # job DBs
        self.DB_JOBS = 'storage/jobs.db' if self.DEBUG else '/var/lib/pulzar/dbs/jobs.db'
        self.DB_NODE_JOBS = 'storage/node_jobs.db' if self.DEBUG else '/var/lib/pulzar/dbs/'

        # Env
        self.REQUEST_METHOD = 'REQUEST_METHOD'
        self.SERVER_NAME = 'SERVER_NAME'
        self.SERVER_PORT = 'SERVER_PORT'
        self.HTTP_HOST = 'HTTP_HOST'
        self.PATH_INFO = 'PATH_INFO'
        self.QUERY_STRING = 'QUERY_STRING'
        self.HTTP_USER_AGENT = 'HTTP_USER_AGENT'
        self.SERVER_PROTOCOL = 'SERVER_PROTOCOL'
        self.CONTENT_LENGTH = 'CONTENT_LENGTH'
        self.CONTENT_TYPE = 'CONTENT_TYPE'
        self.WSGI_INPUT = 'wsgi.input'

        self.POST = 'POST'
        self.PUT = 'PUT'
        self.GET = 'GET'
        self.DELETE = 'DELETE'
        self.JSON_REQUEST = 'application/json'

        # REST admin paths
        self.SKYNET = '/skynet'
        self.REGISTER = self.SKYNET + '/register'
        self.SYNC = self.SKYNET + '/sync'
        # Data flow
        self.ADD_RECORD = self.SKYNET + '/add_record'

        # REGEX
        self.RE_URL_LAST = r'([^/]+$)'
        self.RE_URL_OPTION_ORDER = r'([\w]+)*\/([\w]+)+$'

        # API calls
        self.RE_GET_VALUE = r'\/get_key([\w+|\/{1}]+)?\/([\w|\.]+)$'
        self.RE_DELETE_VALUE = r'\/delete_key([\w+|\/{1}]+)?\/([\w|\.]+)$'
        self.RE_PUT_VALUE = r'\/add_key([\w+|\/{1}]+)?\/([\w|\.]+)$'
        self.RE_THIRD_PARTY = r'/third_party((/\w+)+)'
        self.RE_LAUNCH_JOB = r'\/launch_job([\/\w\d]+)\/([\w\d]+)'
        self.RE_NOTIFICATION_JOB = r'\/notification_job$'
        self.RE_ADMIN = r'/admin((/[\w-]+){1,2})'

        # Type of requests
        self.PULZAR_ERROR = 'pulzar_error'
        self.PULZAR_DEFAULT_MESSAGE = 'default'
        self.USER_ERROR = 'user_error'
        self.AUTODISCOVERY = 'autodiscovery'
        self.REGULAR_GET = 'regular'
        self.REGULAR_PUT = 'put'
        self.TP_RESPONSE = 'third_party_response'
        self.REDIRECT_POST = 'redirect_post'
        self.REDIRECT_PUT = 'redirect_put'
        self.NOTIFY_KEY_TO_MASTER = 'notify2master'
        self.KEY_ALREADY_ADDED = 'duplicated'
        self.KEY_ERROR = 'key_error'
        self.KEY_ADDED = 'key_added'
        self.ADMIN = 'admin'
        self.SKYNET = 'skynet'
        self.SKYNET_RESTORE = 'skynet_restore'
        self.SKYNET_RECORD_ADDED = 'skynet_record_added'
        self.SKYNET_RECORD_RESTORED = 'skynet_record_restored'
        self.SKYNET_RECORD_ALREADY_ADDED = 'skynet_record_already'
        self.KEY_NOT_FOUND = 'key_not_found'
        self.KEY_FOUND = 'key_found'
        self.KEY_FOUND_DELETE = 'key_found_delete'
        self.KEY_DELETED = 'key_deleted'
        self.BACKUP_SCHEDULED = 'backup_scheduled'
        self.SET_TEMPORAL = 'temporal'
        self.JOB_RESPONSE = 'job_response'
        self.JOB_ERROR = 'job_error'
        self.JOB_OK = 'job_ok'
