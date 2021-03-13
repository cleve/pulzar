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
    DEBUG_LEVEL = 'ERROR'
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