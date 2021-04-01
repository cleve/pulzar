from pulzarutils.utils import Utils
from pulzarutils.utils import Constants
from pulzarutils.stream import Config
from pulzarcore.core_db import DB
from pulzarcore.core_rdb import RDB


class NodeUtils:
    """Node helper
    """

    def __init__(self):
        # 20 mins max to consider a volume online.
        self.second_range = 1200
        self.utils = Utils()
        # DB of volumes/keys.
        self.db_volumes = DB(Constants.DB_VOLUME)
        # Jobs database
        self.job_db = RDB(Constants.DB_JOBS)

    def discover_volume(self):
        """Get the volume name

        return: (str)
        """
        server_config = Config(Constants.CONF_PATH)
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
        server_config = Config(Constants.CONF_PATH)
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
            list of nodes
        '''
        job_path = job_path[1:]
        query = f'''SELECT
            job_catalog_node_register.node
        FROM
            job_catalog
        LEFT JOIN job_catalog_node_register ON job_catalog.id = job_catalog_node_register.job_catalog_id
        WHERE job_catalog.path = "{job_path}";
        '''
        list_of_tuples = self.job_db.execute_sql_with_results(query)
        return [node[0].encode() for node in list_of_tuples]
    
    def pick_a_volume2(self, job_path):
        """Volume selection using the workload and the job
        
        Parameter
        ---------
        job_path : str
            String with the path to the job

        Return
        ------
        byte
            URL without port
        """
        nodes_online = []
        volumes = self.db_volumes.get_keys_values()
        node_candidates = self._node_candidates_since_path(job_path)
        current_datetime = self.utils.get_current_datetime()
        # Filtering by online nodes
        for elem in volumes:
            meta_raw = self.utils.decode_byte_to_str(elem[1]).split(':')
            percent = float(meta_raw[1])
            last_update_reported = self.utils.get_datetime_from_string(
                meta_raw[3])
            delta_time = current_datetime - last_update_reported
            # Check availability of node.
            if delta_time.total_seconds() >= self.second_range:
                continue
            # Online nodes with their workload
            nodes_online.append((elem[0], percent))
        
        # Ordering to easy selection
        nodes_online = sorted(nodes_online, key=lambda x : x[1])
        nodes_online = [elem[0] for elem in nodes_online]
        while len(nodes_online) > 0:
            # select the node with low load
            node_selected = nodes_online.pop(0)
            # random_node = self.utils.get_random_element_from_list(nodes_online)
            # nodes_online.remove(random_node)
            if node_selected in node_candidates:
                return node_selected 
        return None
