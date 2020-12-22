from pulzarutils.utils import Utils
from pulzarutils.constants import ReqType
from pulzarutils.file_utils import FileUtils
from pulzarcore.core_request import CoreRequest
from pulzarcore.core_db import DB
from pulzarutils.messenger import Messenger
from pulzarutils.stream import Config


class PutProcess:
    def __init__(self, constants, logger):
        self.TAG = self.__class__.__name__
        self.const = constants
        self.logger = logger
        self.utils = Utils()
        self.db_backup = DB(self.const.DB_BACKUP)
        self.file_utils = FileUtils(self.const)
        self.messenger = Messenger()

    def build_node_response(self, env, root_path, base_name):
        """Build response on where the data was loaded
        """
        url = env[self.const.HTTP_HOST]
        base_url_path = '/get_key'
        return 'http://' + url + base_url_path + root_path + '/' + base_name

    def notify_record_to_master(self, env) -> bool:
        """Report the register creation.
        """
        server_config = Config(self.const.CONF_PATH)
        key = server_config.get_config('server', 'key')
        temporal = '-1'
        query_params = self.utils.extract_query_params(
            'http://fakeurl.com?'+env['QUERY_STRING'])
        if self.const.SET_TEMPORAL in query_params:
            temporal = query_params[self.const.SET_TEMPORAL][0]
        master_url = self.utils.extract_url_data(
            query_params['url'][0])
        # Prod url
        host_url = master_url['host']
        # TODO: MAC support
        if self.const.DEBUG_WIN:
            self.logger.debug(':{}:using docker.for.win.localhost'.format(self.TAG))
            # Forn windows machine
            host_url = 'docker.for.win.localhost'
        # Confirming with master.
        req = CoreRequest(
            host_url,
            master_url['port'],
            self.const.ADD_RECORD
        )
        req.set_type(ReqType.POST)
        req.add_header(
            {
                self.const.PASSPORT: self.utils.encode_base_64(key)
            }
        )
        req.set_path(self.const.ADD_RECORD)
        # We have to send the key, volume and port.
        req.set_payload({
            'key': self.file_utils.get_key(),
            'volume': env[self.const.HTTP_HOST],
            'temporal': temporal
        })
        if not req.make_request():
            # If an error ocurr in the server, we need to delete the file.
            self.file_utils.remove_file()
            py_object = self.utils.json_to_py(req.response)
            self.messenger.code_type = self.const.PULZAR_ERROR
            self.messenger.set_message = py_object['msg']
            self.messenger.mark_as_failed()
            return False
        try:
            self.db_backup.put_value(
                self.file_utils.key.encode(),
                b'1'
            )
        except BaseException as err:
            self.logger.exception(':{}:{}'.format(self.TAG, err))
            self.messenger.code_type = self.const.PULZAR_ERROR
            self.messenger.set_message = str(err)
            self.messenger.mark_as_failed()
            return False
        return True

    def process_request(self, env, start_response, url_path):
        """Entry point to the PUT method
        """
        regex_result = self.utils.get_search_regex(
            url_path, self.const.RE_PUT_VALUE)
        if regex_result:
            try:
                root_path, base_name = regex_result.groups()
                if root_path is None:
                    root_path = ''

                base64_str = self.utils.encode_base_64(
                    root_path + '/' + base_name, True)

                # Url to get the data
                data_url = self.build_node_response(
                    env, root_path, base_name)
                # Trying to create the key-value
                key_to_binary = self.utils.encode_str_to_byte(base64_str)
                self.file_utils.set_key(key_to_binary, base64_str)
                self.file_utils.set_path(root_path)
                key_generated = self.file_utils.read_binary_file(env)
                # Try to reach to master.
                if self.notify_record_to_master(env):
                    self.messenger.code_type = self.const.KEY_ADDED
                    self.messenger.set_response({'url': data_url})
                    self.messenger.http_code = '201 CREATED'
                    self.messenger.set_message = 'key added'

            except BaseException as err:
                self.logger.exception(':{}:{}'.format(self.TAG, err))
                self.messenger.code_type = self.const.USER_ERROR
                self.messenger.set_message = str(err)
                self.messenger.mark_as_failed()

        return self.messenger
