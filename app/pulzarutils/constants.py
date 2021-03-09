from enum import Enum


class Response(Enum):
    JSON = 0
    TEXT = 1
    OPTIONS = 3


class ReqType(Enum):
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4


class Constants:

    DEBUG = False
    # Logger configuration
    # INFO, DEBUG, ERROR
    DEBUG_LEVEL = 'INFO'
    LOG_PATH = 'storage/log/' if DEBUG else '/var/lib/pulzar/log/'
    # To try docker for windows in the same machine
    DEBUG_WIN = False
    VERSION = '1.0.4'
    PASS = 'admin'
    PASSPORT = 'passport'
    EXTENSIONS_DIR = 'master/extensions'
    START_BK = 'start_backup'
    HOST_NAME = 'host'
    # DEV Directory to store data
    DEV_DIRECTORY = 'storage/data'

    # Config
    CONF_HOST = 'host'
    CONF_PORT = 'port'
    CONF_PATH = 'config/server.conf'

    # Databases
    DB_PATH = 'storage/master.db' if DEBUG else '/var/lib/pulzar/dbs/master.db'
    DB_VOLUME = 'storage/volume.db' if DEBUG else '/var/lib/pulzar/dbs/volume.db'
    DB_STATS = 'storage/volume_st.db' if DEBUG else '/var/lib/pulzar/dbs/volume_st.db'
    DB_BACKUP = 'storage/volume_bk.db' if DEBUG else '/var/lib/pulzar/dbs/volume_bk.db'
    DB_NOT_PERMANENT = 'storage/temporal_data.db' if DEBUG else '/var/lib/pulzar/dbs/temporal_data.db'
    # job DBs
    DB_JOBS = 'storage/dbs/jobs.db' if DEBUG else '/var/lib/pulzar/dbs/jobs.db'
    DB_NODE_JOBS = 'storage/dbs/node_jobs.db' if DEBUG else '/var/lib/pulzar/dbs/node_jobs.db'

    # Env
    REQUEST_METHOD = 'REQUEST_METHOD'
    SERVER_NAME = 'SERVER_NAME'
    SERVER_PORT = 'SERVER_PORT'
    HTTP_HOST = 'HTTP_HOST'
    PATH_INFO = 'PATH_INFO'
    QUERY_STRING = 'QUERY_STRING'
    HTTP_USER_AGENT = 'HTTP_USER_AGENT'
    SERVER_PROTOCOL = 'SERVER_PROTOCOL'
    CONTENT_LENGTH = 'CONTENT_LENGTH'
    CONTENT_TYPE = 'CONTENT_TYPE'
    HTTP_PASSPORT = 'HTTP_PASSPORT'
    WSGI_INPUT = 'wsgi.input'

    POST = 'POST'
    PUT = 'PUT'
    GET = 'GET'
    DELETE = 'DELETE'
    JSON_REQUEST = 'application/json'

    # REST admin paths
    SKYNET = '/skynet'
    REGISTER = SKYNET + '/register'
    SYNC = SKYNET + '/sync'
    # Data flow
    ADD_RECORD = SKYNET + '/add_record'

    # REGEX
    RE_URL_LAST = r'([^/]+$)'
    RE_URL_OPTION_ORDER = r'([\w]+)*\/([\w]+)+$'

    # API calls
    RE_GET_STORAGE = r'\/get_node([\w+|\/{1}]+)?\/([\w|\.]+)$'
    RE_GET_VALUE = r'\/get_key([\w+|\/{1}]+)?\/([\w|\.]+)$'
    RE_DELETE_VALUE = r'\/delete_key([\w+|\/{1}]+)?\/([\w|\.]+)$'
    RE_PUT_VALUE = r'\/add_key([\w+|\/{1}]+)?\/([\w|\.]+)$'
    RE_EXTENSION = r'/extension((/\w+)+)'
    RE_LAUNCH_JOB = r'\/launch_job([\/\w\d]+)\/([\w\d]+)'
    RE_CANCEL_JOB = r'\/cancel_job\/([\d]+)$'
    RE_SCHED_JOB_INF = r'\/admin\/(scheduled_jobs|jobs|all_jobs|job_catalog){1}((\/)(failed|ok)){0,1}((\/){1}(\d+)){0,1}([\?|&]limit=(\d+)){0,1}([\?|&]filter=(\w+)){0,1}$'
    RE_NOTIFICATION_JOB = r'\/notification_job$'
    RE_ADMIN = r'/admin((/[\w-]+){1,2})'

    # Type of requests
    OPTIONS = 'options'
    PULZAR_ERROR = 'pulzar_error'
    PULZAR_DEFAULT_MESSAGE = 'default'
    USER_ERROR = 'user_error'
    AUTODISCOVERY = 'autodiscovery'
    REGULAR_GET = 'regular'
    REGULAR_PUT = 'put'
    EXTENSION_RESPONSE = 'extension_response'
    REDIRECT_POST = 'redirect_post'
    GET_NODE = 'get_node'
    REDIRECT_PUT = 'redirect_put'
    NOTIFY_KEY_TO_MASTER = 'notify2master'
    KEY_ALREADY_ADDED = 'duplicated'
    KEY_ERROR = 'key_error'
    KEY_ADDED = 'key_added'
    ADMIN = 'admin'
    SKYNET = 'skynet'
    SKYNET_RESTORE = 'skynet_restore'
    SKYNET_RECORD_ADDED = 'skynet_record_added'
    SKYNET_RECORD_RESTORED = 'skynet_record_restored'
    SKYNET_RECORD_ALREADY_ADDED = 'skynet_record_already'
    KEY_NOT_FOUND = 'key_not_found'
    KEY_FOUND = 'key_found'
    KEY_FOUND_DELETE = 'key_found_delete'
    KEY_DELETED = 'key_deleted'
    BACKUP_SCHEDULED = 'backup_scheduled'
    SET_TEMPORAL = 'temporal'
    JOB_RESPONSE = 'job_response'
    JOB_ERROR = 'job_error'
    JOB_OK = 'job_ok'
    JOB_DETAILS = 'job_details'

    def __init__(self):
        # General
        self.DEBUG = False
        # Logger configuration
        # INFO, DEBUG, ERROR
        self.DEBUG_LEVEL = 'ERROR'
        self.LOG_PATH = 'storage/log/' if self.DEBUG else '/var/lib/pulzar/log/'
        # To try docker for windows in the same machine
        self.DEBUG_WIN = False
        self.VERSION = '1.0.4'
        self.PASS = 'admin'
        self.PASSPORT = 'passport'
        self.EXTENSIONS_DIR = 'master/extensions'
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
        self.DB_JOBS = 'storage/dbs/jobs.db' if self.DEBUG else '/var/lib/pulzar/dbs/jobs.db'
        self.DB_NODE_JOBS = 'storage/dbs/node_jobs.db' if self.DEBUG else '/var/lib/pulzar/dbs/node_jobs.db'

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
        self.HTTP_PASSPORT = 'HTTP_PASSPORT'
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
        self.RE_GET_STORAGE = r'\/get_node([\w+|\/{1}]+)?\/([\w|\.]+)$'
        self.RE_GET_VALUE = r'\/get_key([\w+|\/{1}]+)?\/([\w|\.]+)$'
        self.RE_DELETE_VALUE = r'\/delete_key([\w+|\/{1}]+)?\/([\w|\.]+)$'
        self.RE_PUT_VALUE = r'\/add_key([\w+|\/{1}]+)?\/([\w|\.]+)$'
        self.RE_EXTENSION = r'/extension((/\w+)+)'
        self.RE_LAUNCH_JOB = r'\/launch_job([\/\w\d]+)\/([\w\d]+)'
        self.RE_CANCEL_JOB = r'\/cancel_job\/([\d]+)$'
        self.RE_SCHED_JOB_INF = r'\/admin\/(scheduled_jobs|jobs|all_jobs|job_catalog){1}((\/)(failed|ok)){0,1}((\/){1}(\d+)){0,1}([\?|&]limit=(\d+)){0,1}([\?|&]filter=(\w+)){0,1}$'
        self.RE_NOTIFICATION_JOB = r'\/notification_job$'
        self.RE_ADMIN = r'/admin((/[\w-]+){1,2})'

        # Type of requests
        self.OPTIONS = 'options'
        self.PULZAR_ERROR = 'pulzar_error'
        self.PULZAR_DEFAULT_MESSAGE = 'default'
        self.USER_ERROR = 'user_error'
        self.AUTODISCOVERY = 'autodiscovery'
        self.REGULAR_GET = 'regular'
        self.REGULAR_PUT = 'put'
        self.EXTENSION_RESPONSE = 'extension_response'
        self.REDIRECT_POST = 'redirect_post'
        self.GET_NODE = 'get_node'
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
        self.JOB_DETAILS = 'job_details'
