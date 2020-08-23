from pulzarcore.core_db import DB
from pulzarcore.core_body import Body
from pulzarutils.constants import Constants
from pulzarutils.utils import Utils
from pulzarutils.messenger import Messenger


class Skynet:
    """Internal communication
    """

    def __init__(self, env):
        self.const = Constants()
        self.utils = Utils()
        self.env = env
        self.db_volume = DB(self.const.DB_VOLUME)
        self.master_db = DB(self.const.DB_PATH)
        self.messenger = Messenger()
        # Skynet options
        self.sync_status = self.const.SKYNET + '/sync'
        self.sync_key_added = self.const.SKYNET + '/add_record'
        self.start_backup = self.const.SKYNET + '/start_backup'

    def restore_master(self):
        body = Body()
        params = body.extract_params(self.env)
        key = params[b'key'][0]
        volume = params[b'volume'][0]
        # Saving data
        return self.master_db.put_value(
            key,
            volume
        )

    def save_key_and_volume(self):
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

    def _sync_volume(self):
        response = self.const.SKYNET
        body = Body()
        params = body.extract_params(self.env)
        volume_data = self.db_volume.get_value(params[b'host'][0])
        # Check if volume exists.
        if volume_data is None:
            response = self.const.PULZAR_ERROR
        # Get records registered
        records_in_master = self.master_db.count_values(
            params[b'host'][0], ':')
        print("records_in_master", records_in_master)
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
                self.messenger.code_type = self.const.SKYNET_RECORD_RESTORED
                self.messenger.set_response({'msg': 'ok'})
                return self.messenger

            # This is a confirmation from volume.
            if url_path.find(self.sync_key_added) == 1:
                if self.save_key_and_volume():
                    self.messenger.code_type = self.const.SKYNET_RECORD_ADDED
                    self.messenger.set_message = 'record added'
                    return self.messenger
                self.messenger.code_type = self.const.SKYNET_RECORD_ALREADY_ADDED
                self.messenger.http_code = '406 Not acceptable'
                self.messenger.set_message = 'already added'
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
            print('Error Skynet', err)
            self.messenger.code_type = self.const.PULZAR_ERROR
            self.messenger.mark_as_failed()
            self.messenger.set_message = str(err)

        return self.messenger
