from pulzarutils.utils import Utils
from pulzarutils.stream import Config
from pulzarcore.core_db import DB
from pulzarcore.core_rdb import RDB


class NodeUtils:
    """Node helper
    """

    def __init__(self, constants):
        self.const = constants
        # 20 mins max to consider a volume online.
        self.second_range = 1200
        self.utils = Utils()
        # DB of volumes/keys.
        self.db_volumes = DB(self.const.DB_VOLUME)
        # Jobs database
        self.job_db = RDB(self.const.DB_JOBS)

    def discover_volume(self):
        """Get the volume name

        return: (str)
        """
        server_config = Config(self.const.CONF_PATH)
        volume_port = server_config.get_config('volume', 'port')
        keys = self.db_volumes.get_keys()
        if keys is None:
            return None
        return keys[0].decode() + ':' + volume_port

    def get_port(self):
        """Get port number

        Return
        ------
        int
            port number
        """
        server_config = Config(self.const.CONF_PATH)
        volume_port = server_config.get_config('volume', 'port')
        return volume_port

    def pick_a_volume(self):
        """Volume selection using the load
        
        Return
        ------
        byte
            URL without port
        """
        volumes = self.db_volumes.get_keys_values()
        current_datetime = self.utils.get_current_datetime()
        min_value = 100
        server = None
        for elem in volumes:
            # meta_raw[0] = percent, meta_raw[1] = load
            meta_raw = self.utils.decode_byte_to_str(elem[1]).split(':')
            percent = int(meta_raw[0])
            last_update_reported = self.utils.get_datetime_from_string(
                meta_raw[3])
            delta_time = current_datetime - last_update_reported
            # Check availability of node.
            if delta_time.total_seconds() >= self.second_range:
                continue
            if percent < min_value:
                min_value = percent
                server = elem[0]
        return server

    def _node_candidates_since_path(self, job_path):
        '''Getting nodes
        
        Parameters
        ----------
        job_path : str
            Job path
        
        Return
        ------
        list
            list of tuples with nodes
        '''
        job_path = job_path[1:]
        query = f'''SELECT
            job_catalog_node_register.node
        FROM
            job_catalog
        LEFT JOIN job_catalog_node_register ON job_catalog.id = job_catalog_node_register.job_catalog_id
        WHERE job_catalog.path = "{job_path}";
        '''
        print(query)
        return self.job_db.execute_sql_with_results(query)
    
    def pick_a_volume2(self, job_path):
        """Volume selection using the load and the job
        
        Return
        ------
        byte
            URL without port
        """
        volumes = self.db_volumes.get_keys_values()
        print('=====> ', self._node_candidates_since_path(job_path))
        current_datetime = self.utils.get_current_datetime()
        min_value = 100
        server = None
        for elem in volumes:
            # meta_raw[0] = percent, meta_raw[1] = load
            meta_raw = self.utils.decode_byte_to_str(elem[1]).split(':')
            percent = int(meta_raw[0])
            last_update_reported = self.utils.get_datetime_from_string(
                meta_raw[3])
            delta_time = current_datetime - last_update_reported
            # Check availability of node.
            if delta_time.total_seconds() >= self.second_range:
                continue
            if percent < min_value:
                min_value = percent
                server = elem[0]
        return server
