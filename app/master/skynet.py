from pulzarcore.core_db import DB
from pulzarcore.core_rdb import RDB
from pulzarcore.core_body import Body
from pulzarutils.constants import Constants
from pulzarutils.utils import Utils
from pulzarutils.messenger import Messenger
from pulzarutils.stream import Config


class Skynet:
    """Internal communication
    """

    def __init__(self, env, logger):
        self.TAG = self.__class__.__name__
        self.const = Constants()
        self.utils = Utils()
        self.logger = logger
        self.env = env
        self.db_volume = DB(self.const.DB_VOLUME)
        self.master_db = DB(self.const.DB_PATH)
        self.rdb = RDB(self.const.DB_JOBS)
        self.messenger = Messenger()
        self.server_config = Config(self.const.CONF_PATH)
        self.validated = False
        # Skynet options
        self.sync_status = self.const.SKYNET + '/sync'
        self.sync_key_added = self.const.SKYNET + '/add_record'
        self.start_backup = self.const.SKYNET + '/start_backup'
        self.validate_node(env)

    def validate_node(self, env) -> None:
        '''Using passport to validate node request
        
        Parameters
        ----------
        env : dict
            Environment variables from uwsgi
        '''
        key = self.server_config.get_config('server', 'key')
        if env.get(self.const.HTTP_PASSPORT, None) == None:
            self.validated = False
            self.logger.error(':{}:passport not present'.format(self.TAG))
            return
        self.validated = key == self.utils.decode_string_base_64(env[self.const.HTTP_PASSPORT], True)

    def restore_master(self):
        body = Body()
        params = body.extract_params(self.env)
        key = params[b'key'][0]
        volume = params[b'volume'][0]
        current_datetime = self.utils.get_current_datetime_str()
        composed_value = volume.decode() + ',' + current_datetime
        # Saving data
        return self.master_db.put_value(
            key,
            composed_value.encode()
        )

    def save_key_and_volume(self) -> bool:
        '''Save the key and node into master
        
        Once the node save the info, it sent the notification
        to the master. The info includes:
            - node name, temporary parameter and key
        
        Also datetime is added for search purposes
        '''
        # Passport check
        if not self.validated:
            return False
        # Extract and save value into DB.
        body = Body()
        params = body.extract_params(self.env)
        current_datetime = self.utils.get_current_datetime_str()
        volume = params[b'volume'][0]
        composed_value = volume.decode() + ',' + current_datetime
        # If its temporal, just saving it
        if self.const.SET_TEMPORAL.encode() in params and params[b'temporal'][0] != b'-1':
            temporal_db = DB(self.const.DB_NOT_PERMANENT)
            temporal_db.put_value(
                params[b'key'][0],
                params[b'temporal'][0]
            )
        # Saving data with date.
        return self.master_db.put_value(
            params[b'key'][0],
            composed_value.encode()
        )

    def _synch_catalog(self, catalog, node):
        '''Save catalog using the node information
        
        Parameter
        ---------
        catalog : list
            List with catalog dictionary
        '''
        try:
            # Check if job exists in the current catalog
            for job in catalog:
                job_path = job.get('path')
                query = f"SELECT id FROM job_catalog WHERE path = '{job_path}'"
                result = self.rdb.execute_sql_with_results(query)
                # Register node for the job already registered
                if len(result) == 1:
                    query = f"""
                        INSERT INTO job_catalog_node_register (node, job_catalog_id)
                        SELECT '{node}', {result[0][0]}
                        WHERE NOT EXISTS (SELECT 1 FROM job_catalog_node_register WHERE node = '{node}' AND job_catalog_id = {result[0][0]})
                    """
                    self.rdb.execute_sql(query)
                else:
                    query = 'INSERT INTO job_catalog (path, description, args, category, author) VALUES (?,?,?,?,?)'
                    last_id = self.rdb.execute_sql_insert(
                        query,
                        (
                            job_path,
                            job.get('description'),
                            job.get('args'),
                            job.get('category'),
                            job.get('author')
                        )
                    )
                    if last_id > 0:
                        query = f"""
                        INSERT INTO job_catalog_node_register (node, job_catalog_id)
                        SELECT '{node}', {last_id}
                        WHERE NOT EXISTS (SELECT 1 FROM job_catalog_node_register WHERE node = '{node}' AND job_catalog_id = {last_id})
                        """
                        self.rdb.execute_sql(query)

        except Exception as err:
            print(err)
    
    def _sync_volume(self) -> tuple:
        '''Synch node with master

        The node transfer meta-data to the master
        '''
        # Checking passport
        if not self.validated:
            return

        response = self.const.SKYNET
        body = Body()
        params = body.extract_params(self.env)
        volume_data = self.db_volume.get_value(params[b'host'][0])
        node_name = self.utils.decode_byte_to_str(params[b'host'][0])
        catalog = self.utils.json_to_py(params[b'catalog'][0].decode())
        self._synch_catalog(catalog, node_name)
        # Check if volume exists.
        if volume_data is None:
            response = self.const.PULZAR_ERROR
        # Get records registered
        records_in_master = self.master_db.count_values(
            params[b'host'][0], ':')
        self.logger.debug(':{}:record in master are {}'.format(self.TAG, records_in_master))
        # volume_registered
        current_datetime = self.utils.get_current_datetime_str()
        volume_records = self.utils.decode_byte_to_str(params[b'total'][0])
        volume_records_int = int(volume_records)
        meta_data = self.utils.decode_byte_to_str(
            params[b'percent'][0]) + ':' + self.utils.decode_byte_to_str(params[b'load'][0]) + ':' + volume_records + ':' + current_datetime
        self.db_volume.update_or_insert_value(
            params[b'host'][0],
            self.utils.encode_str_to_byte(meta_data)
        )
        return response, volume_records_int == records_in_master

    def process_request(self, url_path, method):
        try:
            if method != self.const.POST:
                return None

            # Restoring data.
            if url_path.find(self.start_backup) == 1:
                if self.restore_master():
                    self.messenger.code_type = self.const.SKYNET_RECORD_RESTORED
                    self.messenger.set_response({'msg': 'ok'})
                else:
                    self.messenger.code_type = self.const.PULZAR_ERROR
                    self.messenger.set_response({'msg': 'error'})
                return self.messenger

            # This is a confirmation from volume.
            if url_path.find(self.sync_key_added) == 1:
                if self.save_key_and_volume():
                    self.messenger.code_type = self.const.SKYNET_RECORD_ADDED
                    self.messenger.set_message = 'record added'
                    return self.messenger
                self.messenger.code_type = self.const.SKYNET_RECORD_ALREADY_ADDED
                self.messenger.http_code = '406 Not acceptable'
                self.messenger.set_message = 'already added or passport error'
                return self.messenger

            # This is a meta-data received from volume
            if url_path.find(self.sync_status) == 1:
                # Extracting last section of the url
                groups = self.utils.get_search_regex(
                    url_path,
                    self.const.RE_URL_OPTION_ORDER
                )
                if groups is None:
                    self.messenger.code_type = self.const.PULZAR_ERROR
                    self.messenger.mark_as_failed()

                code, synch = self._sync_volume()
                self.messenger.code_type = code
                self.messenger.set_response({'synch': synch})

        except Exception as err:
            self.logger.exception('{}:{}'.format(self.TAG, err))
            self.messenger.code_type = self.const.PULZAR_ERROR
            self.messenger.mark_as_failed()
            self.messenger.set_message = str(err)

        return self.messenger
